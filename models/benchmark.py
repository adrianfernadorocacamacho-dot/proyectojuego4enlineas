"""
Módulo de Benchmark comparativo para Árboles de Juego.

Compara el rendimiento computacional de:
- Árbol Minimax Tradicional (Búsqueda Completa de Nodos).
- Árbol Minimax con Poda Alfa-Beta (Búsqueda Optimizada con Poda de Ramas).
"""

import random
import time
from typing import Any, Dict, List

from .game_model import GameModel
from .minimax_agent import MinimaxAgent


def run_benchmark(num_states: int = 50) -> Dict[str, Any]:
    """
    Ejecuta un benchmark comparando Árbol Minimax Completo vs Árbol con Poda Alfa-Beta.

    Simula tableros representativos del juego y mide:
    - Tiempo de cómputo total en milisegundos.
    - Cantidad promedio de nodos del árbol evaluados.

    Args:
        num_states (int, optional): Cantidad de tableros de prueba a evaluar. Por defecto 50.

    Returns:
        Dict[str, Any]: Métricas de rendimiento comparativo:
            - 'minimax_time_ms': Tiempo total de Minimax tradicional en ms.
            - 'minimax_avg_nodes': Promedio de nodos explorados por Minimax tradicional.
            - 'alphabeta_time_ms': Tiempo total con Poda Alfa-Beta en ms.
            - 'alphabeta_avg_nodes': Promedio de nodos evaluados con Poda Alfa-Beta.
            - 'total_states_tested': Cantidad de estados probados.
    """
    agente_tradicional = MinimaxAgent(usar_poda=False)
    agente_alfa_beta = MinimaxAgent(usar_poda=True)

    # Generar estados semi-aleatorios válidos no terminales
    test_states: List[List[int]] = []
    intentos: int = 0
    while len(test_states) < num_states and intentos < num_states * 4:
        intentos += 1
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
        if not win1 and not win2 and not GameModel.is_draw(board):
            test_states.append(list(board))

    if not test_states:
        test_states = [GameModel.get_initial_board()]

    # 1. Medición para Árbol Minimax Tradicional (Completo)
    start_mm: float = time.time()
    mm_nodes: int = 0
    for state in test_states:
        _, nodes = agente_tradicional.get_best_move(list(state), depth=3)
        mm_nodes += nodes
    mm_time: float = (time.time() - start_mm) * 1000

    # 2. Medición para Árbol Minimax con Poda Alfa-Beta
    start_ab: float = time.time()
    ab_nodes: int = 0
    for state in test_states:
        _, nodes = agente_alfa_beta.get_best_move(list(state), depth=3)
        ab_nodes += nodes
    ab_time: float = (time.time() - start_ab) * 1000

    total_states: int = len(test_states)
    mm_avg: float = round(mm_nodes / total_states, 2) if total_states > 0 else 0.0
    ab_avg: float = round(ab_nodes / total_states, 2) if total_states > 0 else 0.0

    return {
        "minimax_time_ms": round(mm_time, 2),
        "minimax_avg_nodes": mm_avg,
        "alphabeta_time_ms": round(ab_time, 2),
        "alphabeta_avg_nodes": ab_avg,
        # Alias retrocompatibles
        "ml_time_ms": round(ab_time, 2),
        "ml_avg_nodes": ab_avg,
        "total_states_tested": total_states,
    }
