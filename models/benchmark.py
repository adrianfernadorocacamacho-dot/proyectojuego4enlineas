"""
Módulo de Benchmark comparativo para Minimax vs DecisionTree.

Genera las métricas de rendimiento exigidas por el Criterio 5:
- Tiempo de respuesta (ms)
- Cantidad de nodos / estados explorados
- Comparación empírica en tablero 6x6.
"""

import random
import time
from typing import Any, Dict, List

from .game_model import GameModel
from .minimax_agent import MinimaxAgent
from .ml_agent import MLAgent


def run_benchmark(num_states: int = 30) -> Dict[str, Any]:
    """
    Ejecuta un benchmark comparando Minimax Tradicional,
    Minimax con Poda Alfa-Beta y el Árbol de Decisión (Machine Learning).

    Args:
        num_states (int, optional): Número de tableros de prueba.

    Returns:
        Dict[str, Any]: Diccionario con métricas agregadas de rendimiento.
    """
    agente_mm = MinimaxAgent(usar_poda=False)
    agente_ab = MinimaxAgent(usar_poda=True)
    agente_ml = MLAgent()

    # Generar tableros válidos de prueba
    test_states: List[List[int]] = []
    intentos = 0
    while len(test_states) < num_states and intentos < num_states * 4:
        intentos += 1
        board = GameModel.get_initial_board()
        for _ in range(random.randint(2, 8)):
            moves = GameModel.get_valid_moves(board)
            if not moves:
                break
            col = random.choice(moves)
            player = random.choice([1, 2])
            GameModel.drop_piece(board, col, player)

        if (not GameModel.check_win(board, 1)
                and not GameModel.check_win(board, 2)
                and not GameModel.is_draw(board)):
            test_states.append(list(board))

    if not test_states:
        test_states = [GameModel.get_initial_board()]

    total = len(test_states)

    # 1. Medición Minimax Tradicional
    t0 = time.time()
    nodes_mm = 0
    for state in test_states:
        _, n = agente_mm.get_best_move(list(state), depth=3)
        nodes_mm += n
    time_mm = (time.time() - t0) * 1000

    # 2. Medición Minimax con Poda Alfa-Beta
    t0 = time.time()
    nodes_ab = 0
    for state in test_states:
        _, n = agente_ab.get_best_move(list(state), depth=3)
        nodes_ab += n
    time_ab = (time.time() - t0) * 1000

    # 3. Medición Árbol de Decisión (ML)
    t0 = time.time()
    for state in test_states:
        agente_ml.get_move(list(state))
    time_ml = (time.time() - t0) * 1000

    return {
        "minimax_time_ms": round(time_mm, 2),
        "minimax_avg_nodes": round(nodes_mm / total, 1),
        "alphabeta_time_ms": round(time_ab, 2),
        "alphabeta_avg_nodes": round(nodes_ab / total, 1),
        "ml_time_ms": round(time_ml, 2),
        "ml_avg_nodes": 1.0,
        "total_states": total,
    }
