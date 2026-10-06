import os
import time
from typing import Any, Dict, List, Optional

from flask import Flask, Response, jsonify, render_template, request

from models.benchmark import run_benchmark
from models.game_model import GameModel
from models.minimax_agent import MinimaxAgent
from models.ml_agent import MLAgent


app: Flask = Flask(__name__)
minimax_agent: MinimaxAgent = MinimaxAgent()
ml_agent: MLAgent = MLAgent()


@app.route("/")
def index() -> str:
    """
    Controlador de la página principal. Renderiza la interfaz de usuario.

    Returns:
        str: Plantilla HTML renderizada (templates/index.html).
    """
    return render_template("index.html")


@app.route("/api/human-move", methods=["POST"])
def human_move() -> Response:
    """
    Procesa el movimiento realizado por el jugador humano en el tablero.

    Espera un JSON en el cuerpo con:
        - board (List[int]): Vector del tablero (16 posiciones).
        - col (int): Columna seleccionada por el usuario (0 a 3).
        - player (int, opcional): ID del jugador (1 por defecto).

    Returns:
        Response: Respuesta JSON con el resultado de la jugada:
            - success (bool): True si el movimiento fue legal.
            - board (List[int]): Tablero actualizado.
            - win (bool): True si el movimiento produjo victoria.
            - draw (bool): True si la partida terminó en empate.
    """
    data: Dict[str, Any] = request.get_json(force=True) or {}
    board: List[int] = data.get("board", [])
    col: int = int(data.get("col", -1))
    player: int = int(data.get("player", 1))

    success: bool = GameModel.drop_piece(board, col, player)
    win: bool = GameModel.check_win(board, player)
    draw: bool = GameModel.is_draw(board)

    return jsonify({
        "success": success,
        "board": board,
        "win": win,
        "draw": draw,
    })


@app.route("/api/minimax-move", methods=["POST"])
def minimax_move() -> Response:
    """
    Calcula y ejecuta la mejor jugada para la IA usando el algoritmo Minimax.

    Espera un JSON en el cuerpo con:
        - board (List[int]): Vector del estado actual del tablero.

    Returns:
        Response: Respuesta JSON con la jugada efectuada y métricas:
            - board (List[int]): Tablero resultante tras colocar la ficha.
            - col (Optional[int]): Columna elegida por Minimax.
            - win (bool): True si la IA ganó con este movimiento.
            - draw (bool): True si la partida quedó en tablas.
            - time_ms (float): Tiempo de cómputo en milisegundos.
            - nodes (int): Nodos del árbol evaluados durante la búsqueda.
    """
    data: Dict[str, Any] = request.get_json(force=True) or {}
    board: List[int] = data.get("board", [])

    start: float = time.time()
    best_col, nodes = minimax_agent.get_best_move(board)
    elapsed: float = (time.time() - start) * 1000

    win: bool = False
    draw: bool = False

    if best_col is not None:
        GameModel.drop_piece(board, best_col, 2)
        win = GameModel.check_win(board, 2)
        draw = GameModel.is_draw(board)
    else:
        draw = True

    return jsonify({
        "board": board,
        "col": best_col,
        "win": win,
        "draw": draw,
        "time_ms": elapsed,
        "nodes": nodes,
    })


@app.route("/api/ml-move", methods=["POST"])
def ml_move() -> Response:
    """
    Calcula y ejecuta la jugada para la IA mediante el Árbol de Decisión (ML).

    Espera un JSON en el cuerpo con:
        - board (List[int]): Vector del estado actual del tablero.

    Returns:
        Response: Respuesta JSON con la jugada efectuada y métricas:
            - board (List[int]): Tablero resultante tras colocar la ficha.
            - col (Optional[int]): Columna predicha por el clasificador.
            - win (bool): True si la IA ganó con este movimiento.
            - draw (bool): True si la partida quedó en tablas.
            - time_ms (float): Tiempo de inferencia en milisegundos.
            - nodes (int): Nodos evaluados (1 por predicción O(1)).
    """
    data: Dict[str, Any] = request.get_json(force=True) or {}
    board: List[int] = data.get("board", [])

    start: float = time.time()
    col, nodes = ml_agent.get_move(board)
    elapsed: float = (time.time() - start) * 1000

    win: bool = False
    draw: bool = False

    if col is not None:
        GameModel.drop_piece(board, col, 2)
        win = GameModel.check_win(board, 2)
        draw = GameModel.is_draw(board)
    else:
        draw = True

    return jsonify({
        "board": board,
        "col": col,
        "win": win,
        "draw": draw,
        "time_ms": elapsed,
        "nodes": nodes,
    })


@app.route("/api/benchmark", methods=["GET"])
def benchmark() -> Response:
    """
    Endpoint para ejecutar el benchmark comparativo de Minimax vs DecisionTree.

    Returns:
        Response: Respuesta JSON que contiene las métricas agregadas de
        tiempo (ms) y nodos explorados para ambos enfoques de IA.
    """
    res: Dict[str, Any] = run_benchmark()
    return jsonify(res)


if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    app.run(debug=True)
