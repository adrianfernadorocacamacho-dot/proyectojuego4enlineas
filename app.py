import os
import sys
import time
from typing import Any, Dict, List

import werkzeug
from flask import Flask, Response, jsonify, render_template, request

if not hasattr(werkzeug, "__version__"):
    try:
        import importlib.metadata
        werkzeug.__version__ = importlib.metadata.version("werkzeug")
    except Exception:
        werkzeug.__version__ = "3.1.3"

# Asegurar que arbolBinario esté en el path
sys.path.append(os.path.join(os.path.dirname(__file__), "arbolBinario"))

from models.benchmark import run_benchmark  # noqa: E402
from models.game_model import GameModel  # noqa: E402
from models.minimax_agent import MinimaxAgent  # noqa: E402
from models.ml_agent import MLAgent  # noqa: E402


app: Flask = Flask(__name__)

# Agentes correspondientes a los 3 modos de juego
minimax_agent: MinimaxAgent = MinimaxAgent(usar_poda=False)
alphabeta_agent: MinimaxAgent = MinimaxAgent(usar_poda=True)
ml_agent: MLAgent = MLAgent()


@app.route("/")
def index() -> str:
    """Controlador de la página principal. Renderiza el tablero."""
    return render_template("index.html")


@app.route("/api/human-move", methods=["POST"])
def human_move() -> Response:
    """Procesa el movimiento realizado por el jugador humano."""
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
    """Modo 1: Minimax Tradicional con Backtracking y Árbol Binario."""
    data: Dict[str, Any] = request.get_json(force=True) or {}
    board: List[int] = data.get("board", [])

    t0 = time.time()
    best_col, nodes = minimax_agent.get_best_move(board, depth=3)
    elapsed_ms = round((time.time() - t0) * 1000, 2)

    win = False
    draw = False

    if best_col is not None:
        GameModel.drop_piece(board, best_col, 2)
        win = GameModel.check_win(board, 2)
        draw = GameModel.is_draw(board)
    else:
        draw = True

    print(
        f"[DEBUG BACKTRACKING] Modo 1 (Minimax): {nodes} estados "
        f"en {elapsed_ms} ms -> Decisión: Columna {best_col}"
    )

    return jsonify({
        "board": board,
        "col": best_col,
        "win": win,
        "draw": draw,
        "time_ms": elapsed_ms,
        "nodes": nodes,
    })


@app.route("/api/alphabeta-move", methods=["POST"])
def alphabeta_move() -> Response:
    """Modo 2: Minimax con Poda Alfa-Beta (Desafío Extendido opcional)."""
    data: Dict[str, Any] = request.get_json(force=True) or {}
    board: List[int] = data.get("board", [])

    t0 = time.time()
    col, nodes = alphabeta_agent.get_best_move(board, depth=3)
    elapsed_ms = round((time.time() - t0) * 1000, 2)

    win = False
    draw = False

    if col is not None:
        GameModel.drop_piece(board, col, 2)
        win = GameModel.check_win(board, 2)
        draw = GameModel.is_draw(board)
    else:
        draw = True

    print(
        f"[DEBUG PODA ALFA-BETA] Modo 2 (Alfa-Beta): {nodes} estados "
        f"en {elapsed_ms} ms -> Decisión: Columna {col}"
    )

    return jsonify({
        "board": board,
        "col": col,
        "win": win,
        "draw": draw,
        "time_ms": elapsed_ms,
        "nodes": nodes,
    })


@app.route("/api/ml-move", methods=["POST"])
def ml_move() -> Response:
    """Modo 3: Árbol de Decisión ML (DecisionTreeClassifier)."""
    data: Dict[str, Any] = request.get_json(force=True) or {}
    board: List[int] = data.get("board", [])

    t0 = time.time()
    col: int = ml_agent.get_move(board)
    elapsed_ms = round((time.time() - t0) * 1000, 2)

    win = False
    draw = False

    if col is not None:
        GameModel.drop_piece(board, col, 2)
        win = GameModel.check_win(board, 2)
        draw = GameModel.is_draw(board)
    else:
        draw = True

    print(
        f"[DEBUG ML] Modo 3 (DecisionTreeClassifier): Inferencia O(1) "
        f"en {elapsed_ms} ms -> Decisión: Columna {col}"
    )

    return jsonify({
        "board": board,
        "col": col,
        "win": win,
        "draw": draw,
        "time_ms": elapsed_ms,
        "nodes": 1,
    })


@app.route("/api/ml-rules", methods=["GET"])
def ml_rules() -> Response:
    """Retorna las reglas de decisión del DecisionTreeClassifier."""
    rules: str = ml_agent.get_rules_text(max_depth=4)
    return jsonify({
        "rules": rules,
        "dataset_samples": "7,000+ muestras con 1,500 simulaciones",
        "algorithm": "DecisionTreeClassifier (scikit-learn)",
    })


@app.route("/api/benchmark", methods=["GET"])
def benchmark() -> Response:
    """Ejecuta el benchmark comparativo para justificar el reporte."""
    res: Dict[str, Any] = run_benchmark(num_states=25)
    return jsonify(res)


if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    app.run(debug=True)
