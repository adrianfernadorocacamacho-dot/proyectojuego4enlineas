"""
Módulo del agente inteligente para Conecta 4 (4x4).

Utiliza la estructura de datos tradicional de Árbol Binario de Búsqueda
(arbolBinario.ClaseArbolBinario y arbolBinario.ClaseNodo).
"""

import math
from typing import List, Optional, Tuple, Union

from arbolBinario.ClaseArbolBinario import ArbolBinario
from arbolBinario.Jugada import Jugada
from .game_model import GameModel


class MinimaxAgent:
    """
    Agente que utiliza un Árbol Binario tradicional (ArbolBinario y ClaseNodo)
    para organizar y seleccionar las mejores jugadas de Conecta 4.

    Funcionamiento fácil de explicar:
    1. Para cada columna válida, se evalúa la jugada mediante Minimax (con o sin Poda Alfa-Beta).
    2. Cada jugada evaluada (puntuación y columna) se inserta en el ArbolBinario usando `insertar()`.
    3. Como es un Árbol Binario de Búsqueda (BST), la jugada con mayor puntuación se encuentra
       directamente en el extremo derecho del árbol (o al final del recorrido inOrden()).
    """

    def __init__(self, usar_poda: bool = False) -> None:
        """
        Inicializa el agente Minimax.

        Args:
            usar_poda (bool): True para activar Poda Alfa-Beta, False para búsqueda completa.
        """
        self.usar_poda: bool = usar_poda
        self.nodes_evaluated: int = 0
        self.arbol_decisiones: Optional[ArbolBinario] = None

    def get_best_move(
        self, board: List[int], depth: int = 4
    ) -> Tuple[Optional[int], int]:
        """
        Evalúa las columnas y las almacena en una instancia de ArbolBinario.

        Args:
            board (List[int]): Estado actual del tablero (16 posiciones).
            depth (int, optional): Profundidad de búsqueda. Por defecto 4.

        Returns:
            Tuple[Optional[int], int]: Columna óptima elegida y nodos explorados.
        """
        self.nodes_evaluated = 0
        valid_moves: List[int] = GameModel.get_valid_moves(board)

        if not valid_moves:
            return None, 0

        # Crear una nueva instancia de ArbolBinario tradicional
        self.arbol_decisiones = ArbolBinario()

        for col in valid_moves:
            GameModel.drop_piece(board, col, 2)
            if self.usar_poda:
                score = self.minimax_alfa_beta(board, depth - 1, -math.inf, math.inf, False)
            else:
                score = self.minimax(board, depth - 1, False)
            GameModel.undo_move(board, col)

            # Insertar en el Árbol Binario con el método insertar()
            jugada = Jugada(puntaje=score, columna=col)
            self.arbol_decisiones.insertar(jugada)

        # En el Árbol Binario de Búsqueda, la mejor jugada es el nodo mayor
        mejor_jugada: Optional[Jugada] = self.arbol_decisiones.obtenerMayor()
        best_col: int = mejor_jugada.columna if mejor_jugada is not None else valid_moves[0]

        return best_col, self.nodes_evaluated

    def minimax(
        self, board: List[int], depth: int, is_maximizing: bool
    ) -> Union[int, float]:
        """
        Algoritmo Minimax tradicional (recursivo con backtracking).
        """
        self.nodes_evaluated += 1

        if GameModel.check_win(board, 2):
            return 10 + depth
        if GameModel.check_win(board, 1):
            return -10 - depth
        if GameModel.is_draw(board) or depth == 0:
            return 0

        valid_moves: List[int] = GameModel.get_valid_moves(board)

        if is_maximizing:
            best_score: float = -math.inf
            for col in valid_moves:
                GameModel.drop_piece(board, col, 2)
                score = self.minimax(board, depth - 1, False)
                GameModel.undo_move(board, col)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for col in valid_moves:
                GameModel.drop_piece(board, col, 1)
                score = self.minimax(board, depth - 1, True)
                GameModel.undo_move(board, col)
                best_score = min(best_score, score)
            return best_score

    def minimax_alfa_beta(
        self, board: List[int], depth: int, alfa: float, beta: float, is_maximizing: bool
    ) -> Union[int, float]:
        """
        Algoritmo Minimax con Poda Alfa-Beta para descartar ramas innecesarias.
        """
        self.nodes_evaluated += 1

        if GameModel.check_win(board, 2):
            return 10 + depth
        if GameModel.check_win(board, 1):
            return -10 - depth
        if GameModel.is_draw(board) or depth == 0:
            return 0

        valid_moves: List[int] = GameModel.get_valid_moves(board)

        if is_maximizing:
            best_score: float = -math.inf
            for col in valid_moves:
                GameModel.drop_piece(board, col, 2)
                score = self.minimax_alfa_beta(board, depth - 1, alfa, beta, False)
                GameModel.undo_move(board, col)
                best_score = max(best_score, score)
                alfa = max(alfa, best_score)
                if beta <= alfa:
                    break
            return best_score
        else:
            best_score = math.inf
            for col in valid_moves:
                GameModel.drop_piece(board, col, 1)
                score = self.minimax_alfa_beta(board, depth - 1, alfa, beta, True)
                GameModel.undo_move(board, col)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alfa:
                    break
            return best_score
