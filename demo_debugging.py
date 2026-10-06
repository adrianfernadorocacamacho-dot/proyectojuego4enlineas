"""
Script de Demostración y Debugging Metodológico para el Docente.

Cumple con las Recomendaciones Metodológicas del Docente:
1. Semana 2: Imprime la traza de llamadas recursivas y Backtracking.
2. Semana 3: Exporta reglas con DecisionTreeClassifier (export_text).
3. Desafío Extendido: Demuestra Poda Alfa-Beta en tablero 6x6.
"""

import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Configurar rutas
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "arbolBinario")))

from models.game_model import GameModel  # noqa: E402
from models.minimax_agent import MinimaxAgent  # noqa: E402
from models.ml_agent import MLAgent  # noqa: E402


def demo_semana_2_backtracking():
    print("\n" + "=" * 75)
    print("DEMOSTRACIÓN 1: SESIÓN DE DEBUGGING Y TRAZA RECURSIVA (Semana 2)")
    print("=" * 75)
    print("Objetivo: Visualizar recursión y restauración con undo_move().")
    print("-" * 75)

    # Crear tablero 6x6 con fichas iniciales
    board = GameModel.get_initial_board()
    GameModel.drop_piece(board, 2, 1)  # Humano
    GameModel.drop_piece(board, 2, 2)  # IA
    GameModel.drop_piece(board, 3, 1)  # Humano

    agent = MinimaxAgent(usar_poda=False)

    # Imprimir traza recursiva paso a paso
    agent.trace_backtracking(board, depth=2)

    # Búsqueda completa e inspección de ArbolBinario tradicional
    best_col, nodes = agent.get_best_move(board, depth=2)
    print(f"\n[DECISIÓN FINAL] Columna: {best_col} (Nodos: {nodes})")

    if agent.arbol_decisiones is not None:
        print("\n[ESTRUCTURA DEL ÁRBOL BINARIO DE BÚSQUEDA (BST)]")
        print(agent.arbol_decisiones.obtenerEstructuraVisual())
        print(f"In-Orden: {agent.arbol_decisiones.inOrden()}")
        print(f"Mayor valor: {agent.arbol_decisiones.obtenerMayor()}")


def demo_semana_3_reglas_ml():
    print("\n" + "=" * 75)
    print("DEMOSTRACIÓN 2: VISUALIZACIÓN DE REGLAS ML (Semana 3)")
    print("=" * 75)
    print("Objetivo: Reglas del DecisionTreeClassifier con export_text.")
    print("-" * 75)

    ml = MLAgent()
    rules = ml.get_rules_text(max_depth=3)
    print(rules)


def demo_desafio_extendido_poda():
    print("\n" + "=" * 75)
    print("DEMOSTRACIÓN 3: DESAFÍO EXTENDIDO - PODA ALFA-BETA EN 6x6")
    print("=" * 75)
    print("Objetivo: Comparar Minimax tradicional vs Poda Alfa-Beta.")
    print("-" * 75)

    board = GameModel.get_initial_board()
    GameModel.drop_piece(board, 2, 1)
    GameModel.drop_piece(board, 3, 2)
    GameModel.drop_piece(board, 3, 1)

    agent_trad = MinimaxAgent(usar_poda=False)
    agent_poda = MinimaxAgent(usar_poda=True)

    t0 = time.time()
    col_trad, nodes_trad = agent_trad.get_best_move(board, depth=3)
    t_trad = (time.time() - t0) * 1000

    t0 = time.time()
    col_poda, nodes_poda = agent_poda.get_best_move(board, depth=3)
    t_poda = (time.time() - t0) * 1000

    reduction = round((1 - (nodes_poda / max(1, nodes_trad))) * 100, 1)

    print(f"Minimax Tradicional: Col {col_trad} | Nodos: {nodes_trad:4d} "
          f"| Tiempo: {t_trad:6.2f} ms")
    print(f"Poda Alfa-Beta:      Col {col_poda} | Nodos: {nodes_poda:4d} "
          f"| Tiempo: {t_poda:6.2f} ms")
    print(f"-> Reducción de nodos evaluados gracias a poda: {reduction}%")
    print(f"-> Misma jugada óptima garantizada: {col_trad == col_poda}")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    print("\n" + "*" * 75)
    print("  EJECUCIÓN DE DEBUGGING METODOLÓGICO: 4 EN RAYA 6x6 (MVC + ML)")
    print("*" * 75)
    demo_semana_2_backtracking()
    demo_semana_3_reglas_ml()
    demo_desafio_extendido_poda()
