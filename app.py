import os
import sys
import time
from typing import Any, Dict, List

import werkzeug
if not hasattr(werkzeug, "__version__"):
    try:
        import importlib.metadata
        werkzeug.__version__ = importlib.metadata.version("werkzeug")
    except Exception:
        werkzeug.__version__ = "3.1.3"

# Asegurar que arbolBinario esté en el path (similar al repo de referencia)
sys.path.append(os.path.join(os.path.dirname(__file__), "arbolBinario"))

from flask import Flask, Response, jsonify, render_template, request

from arbolBinario.ClaseArbolBinario import ArbolBinario
from arbolBinario.ClaseNodo import ClaseNodo
from models.benchmark import run_benchmark
from models.game_model import GameModel
from models.minimax_agent import MinimaxAgent

app: Flask = Flask(__name__)

# Agentes basados en la estructura tradicional de ArbolBinario
minimax_agent: MinimaxAgent = MinimaxAgent(usar_poda=False)
alphabeta_agent: MinimaxAgent = MinimaxAgent(usar_poda=True)


@app.route("/")
def index() -> str:
    """
    Controlador de la página principal. Renderiza la interfaz de usuario.
    """
    return render_template("index.html")


@app.route("/api/human-move", methods=["POST"])
def human_move() -> Response:
    """
    Procesa el movimiento realizado por el jugador humano en el tablero.
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
    Calcula y ejecuta la jugada para la IA usando Minimax tradicional,
    almacenando las opciones evaluadas en una instancia de ArbolBinario.
    """
    data: Dict[str, Any] = request.get_json(force=True) or {}
    board: List[int] = data.get("board", [])

    start: float = time.time()
    best_col, nodes = minimax_agent.get_best_move(board, depth=4)
    elapsed: float = (time.time() - start) * 1000

    win: bool = False
    draw: bool = False

    if best_col is not None:
        GameModel.drop_piece(board, best_col, 2)
        win = GameModel.check_win(board, 2)
        draw = GameModel.is_draw(board)
    else:
        draw = True

    # Métricas del Árbol Binario
    tree = minimax_agent.arbol_decisiones
    tree_info: Dict[str, Any] = {}
    if tree is not None:
        tree_info = {
            "total_nodos": tree.cantidadNodos(),
            "altura": tree.altura(),
            "inorden": [str(x) for x in tree.inOrden()],
            "ascii": tree.obtenerEstructuraVisual(),
        }

    return jsonify({
        "board": board,
        "col": best_col,
        "win": win,
        "draw": draw,
        "time_ms": elapsed,
        "nodes": nodes,
        "tree_info": tree_info,
    })


@app.route("/api/alphabeta-move", methods=["POST"])
@app.route("/api/ml-move", methods=["POST"])
def alphabeta_move() -> Response:
    """
    Calcula y ejecuta la jugada para la IA usando Minimax con Poda Alfa-Beta,
    insertando las opciones evaluadas en ArbolBinario.
    """
    data: Dict[str, Any] = request.get_json(force=True) or {}
    board: List[int] = data.get("board", [])

    start: float = time.time()
    col, nodes = alphabeta_agent.get_best_move(board, depth=4)
    elapsed: float = (time.time() - start) * 1000

    win: bool = False
    draw: bool = False

    if col is not None:
        GameModel.drop_piece(board, col, 2)
        win = GameModel.check_win(board, 2)
        draw = GameModel.is_draw(board)
    else:
        draw = True

    # Métricas del Árbol Binario
    tree = alphabeta_agent.arbol_decisiones
    tree_info: Dict[str, Any] = {}
    if tree is not None:
        tree_info = {
            "total_nodos": tree.cantidadNodos(),
            "altura": tree.altura(),
            "inorden": [str(x) for x in tree.inOrden()],
            "ascii": tree.obtenerEstructuraVisual(),
        }

    return jsonify({
        "board": board,
        "col": col,
        "win": win,
        "draw": draw,
        "time_ms": elapsed,
        "nodes": nodes,
        "tree_info": tree_info,
    })


@app.route("/api/benchmark", methods=["GET"])
def benchmark() -> Response:
    """
    Endpoint para ejecutar el benchmark comparativo.
    """
    res: Dict[str, Any] = run_benchmark()
    return jsonify(res)


if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    app.run(debug=True)
