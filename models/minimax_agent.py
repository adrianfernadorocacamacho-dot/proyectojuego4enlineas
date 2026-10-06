import math
from typing import List, Optional, Tuple, Union

from .game_model import GameModel


class MinimaxAgent:
    """
    Agente que utiliza Búsqueda Exhaustiva (Minimax con Backtracking).

    Atributos:
        nodes_evaluated (int): Contador de nodos/estados explorados en el árbol.
    """

    def __init__(self) -> None:
        """
        Inicializa una nueva instancia del agente Minimax.

        Returns:
            None
        """
        self.nodes_evaluated: int = 0

    def get_best_move(
        self, board: List[int], depth: int = 4
    ) -> Tuple[Optional[int], int]:
        """
        Calcula y selecciona la mejor columna mediante el algoritmo Minimax.

        Args:
            board (List[int]): Estado actual del tablero (16 posiciones).
            depth (int, optional): Profundidad límite de búsqueda. Por defecto 4.

        Returns:
            Tuple[Optional[int], int]: Tupla con el índice de columna elegida
            (o None si no hay movimientos legales) y el número total de nodos
            evaluados.
        """
        self.nodes_evaluated = 0
        best_score: float = -math.inf
        best_col: Optional[int] = None
        valid_moves: List[int] = GameModel.get_valid_moves(board)

        if not valid_moves:
            return None, 0

        for col in valid_moves:
            GameModel.drop_piece(board, col, 2)
            score: Union[int, float] = self.minimax(board, depth - 1, False)
            GameModel.undo_move(board, col)

            if score > best_score:
                best_score = score
                best_col = col

        if best_col is None:
            best_col = valid_moves[0]

        return best_col, self.nodes_evaluated

    def minimax(
        self, board: List[int], depth: int, is_maximizing: bool
    ) -> Union[int, float]:
        """
        Función recursiva que evalúa el valor Minimax de un estado del árbol.

        Args:
            board (List[int]): Estado actual del tablero evaluado.
            depth (int): Nivel de profundidad restante por explorar.
            is_maximizing (bool): True si es el turno de la IA (maximizar),
                False si es el turno del oponente humano (minimizar).

        Returns:
            Union[int, float]: Puntuación heurística o terminal asignada al
            estado.
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
                score: Union[int, float] = self.minimax(board, depth - 1, False)
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
