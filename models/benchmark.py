import random
import time
from typing import Any, Dict, List

from .game_model import GameModel
from .minimax_agent import MinimaxAgent
from .ml_agent import MLAgent


def run_benchmark() -> Dict[str, Any]:
    """
    Ejecuta un benchmark comparando Minimax vs Árbol de Decisión (Machine Learning).

    Simula 100 tableros representativos y mide:
    - Tiempo de cómputo en milisegundos.
    - Cantidad promedio de nodos/estados evaluados.

    Returns:
        Dict[str, Any]: Diccionario con las métricas de rendimiento:
            - 'minimax_time_ms' (float): Tiempo total de Minimax en ms.
            - 'minimax_avg_nodes' (float): Promedio de nodos explorados por Minimax.
            - 'ml_time_ms' (float): Tiempo total de inferencia ML en ms.
            - 'ml_avg_nodes' (int): Nodos evaluados por ML (fijo en 1).
            - 'total_states_tested' (int): Número total de tableros testeados.
    """
    minimax: MinimaxAgent = MinimaxAgent()
    ml: MLAgent = MLAgent()

    # Generar 100 estados semi-aleatorios no terminales
    test_states: List[List[int]] = []
    for _ in range(100):
        board: List[int] = GameModel.get_initial_board()
        for _ in range(random.randint(2, 6)):
            moves: List[int] = GameModel.get_valid_moves(board)
            if not moves:
                break

            col: int = random.choice(moves)
            player: int = random.choice([1, 2])
            GameModel.drop_piece(board, col, player)

        win1: bool = GameModel.check_win(board, 1)
        win2: bool = GameModel.check_win(board, 2)
        if not win1 and not win2:
            test_states.append(list(board))

    # Medición para Minimax
    start_mm: float = time.time()
    mm_nodes: int = 0
    for state in test_states:
        b: List[int] = list(state)
        _, nodes = minimax.get_best_move(b, depth=4)
        mm_nodes += nodes
    mm_time: float = (time.time() - start_mm) * 1000

    # Medición para Machine Learning
    start_ml: float = time.time()
    for state in test_states:
        ml.get_move(state)
    ml_time: float = (time.time() - start_ml) * 1000

    total_states: int = len(test_states)
    avg_nodes: float = (mm_nodes / total_states) if total_states > 0 else 0.0

    return {
        "minimax_time_ms": round(mm_time, 2),
        "minimax_avg_nodes": round(avg_nodes, 2),
        "ml_time_ms": round(ml_time, 2),
        "ml_avg_nodes": 1,
        "total_states_tested": total_states,
    }
