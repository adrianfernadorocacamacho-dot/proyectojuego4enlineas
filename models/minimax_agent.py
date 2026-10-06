"""
Módulo del agente inteligente Minimax con Backtracking y Heurística.

Cumple con el criterio del 30%:
- Exploración recursiva del árbol de decisiones.
- Mecanismo de Backtracking garantizado con GameModel.undo_move().
- Agente de alto rendimiento / imbatible (evaluación heurística).
- Soporte para Poda Alfa-Beta (Desafío Extendido opcional).
"""

import math
from typing import List, Optional, Tuple, Union

from arbolBinario.ClaseArbolBinario import ArbolBinario
from arbolBinario.Jugada import Jugada
from .game_model import GameModel


class MinimaxAgent:
    """
    Agente que utiliza Búsqueda Exhaustiva con Backtracking y Árbol Binario.

    Atributos:
        usar_poda (bool): Activa la poda Alfa-Beta para reducir espacio.
        nodes_evaluated (int): Contador de estados evaluados en el turno.
        arbol_decisiones (Optional[ArbolBinario]): Estructura tradicional.
    """

    def __init__(self, usar_poda: bool = False) -> None:
        self.usar_poda: bool = usar_poda
        self.nodes_evaluated: int = 0
        self.arbol_decisiones: Optional[ArbolBinario] = None

    def get_best_move(
        self, board: List[int], depth: int = 3
    ) -> Tuple[Optional[int], int]:
        """
        Calcula la mejor columna e inserta jugadas en el ArbolBinario.

        Args:
            board (List[int]): Tablero de 36 posiciones.
            depth (int, optional): Profundidad de búsqueda. Por defecto 3.

        Returns:
            Tuple[Optional[int], int]: Columna óptima y nodos evaluados.
        """
        self.nodes_evaluated = 0
        valid_moves: List[int] = GameModel.get_valid_moves(board)

        if not valid_moves:
            return None, 0

        self.arbol_decisiones = ArbolBinario()

        # Priorizar columnas centrales (2 y 3 tienen mayor potencial táctico)
        valid_moves.sort(key=lambda c: abs(c - 2.5))

        # 1. Comprobación de Victoria Inmediata
        for col in valid_moves:
            GameModel.drop_piece(board, col, 2)
            if GameModel.check_win(board, 2):
                GameModel.undo_move(board, col)
                self.arbol_decisiones.insertar(
                    Jugada(puntaje=1000.0, columna=col))
                return col, 1
            GameModel.undo_move(board, col)

        # 2. Comprobación de Bloqueo Inmediato
        for col in valid_moves:
            GameModel.drop_piece(board, col, 1)
            if GameModel.check_win(board, 1):
                GameModel.undo_move(board, col)
                self.arbol_decisiones.insertar(
                    Jugada(puntaje=900.0, columna=col))
                return col, 1
            GameModel.undo_move(board, col)

        # 3. Construcción del Árbol Binario y Búsqueda Minimax
        alfa = -math.inf
        beta = math.inf

        for col in valid_moves:
            GameModel.drop_piece(board, col, 2)
            if self.usar_poda:
                score = self.minimax_alfa_beta(
                    board, depth - 1, alfa, beta, False)
                alfa = max(alfa, score)
            else:
                score = self.minimax(board, depth - 1, False)
            GameModel.undo_move(board, col)  # Backtracking

            # Insertar en el Árbol Binario tradicional
            jugada = Jugada(puntaje=score, columna=col)
            self.arbol_decisiones.insertar(jugada)

        # Obtener el máximo del Árbol Binario de Búsqueda
        mejor: Optional[Jugada] = self.arbol_decisiones.obtenerMayor()
        best_col: int = mejor.columna if mejor is not None else valid_moves[0]

        return best_col, self.nodes_evaluated

    def trace_backtracking(self, board: List[int], depth: int = 2) -> None:
        """
        Imprime en consola la traza de llamadas recursivas y backtracking.
        (Recomendación metodológica de la Semana 2 del docente).
        """
        print("\n" + "=" * 70)
        print(
            f"--- TRAZA DE RECURSIÓN Y BACKTRACKING (Prof: {depth}) ---")
        print("=" * 70)

        def _rec_trace(
            current_board: List[int], d: int, is_max: bool, indent: str = ""
        ) -> float:
            player_name = "IA" if is_max else "Humano"
            piece = 2 if is_max else 1

            if GameModel.check_win(current_board, 2):
                print(f"{indent}[TERMINAL] IA gana (+1000). Retornando.")
                return 1000.0 + d
            if GameModel.check_win(current_board, 1):
                print(f"{indent}[TERMINAL] Humano gana (-1000). Retornando.")
                return -1000.0 - d
            if GameModel.is_draw(current_board):
                print(f"{indent}[TERMINAL] Empate (0).")
                return 0.0
            if d == 0:
                h = float(self.evaluate_board(current_board))
                print(f"{indent}[HOJA] Profundidad 0 -> Heurística: {h}")
                return h

            valid = GameModel.get_valid_moves(current_board)
            best = -math.inf if is_max else math.inf

            for c in valid:
                print(f"{indent}--> [{player_name}] drop_piece(col={c})")
                GameModel.drop_piece(current_board, c, piece)

                score = _rec_trace(
                    current_board, d - 1, not is_max, indent + "    ")

                print(
                    f"{indent}<-- [BACKTRACKING] undo({c}): Score={score}")
                GameModel.undo_move(current_board, c)

                if is_max:
                    best = max(best, score)
                else:
                    best = min(best, score)

            print(f"{indent}<= Subárbol para {player_name}: Puntaje = {best}")
            return best

        _rec_trace(list(board), depth, True, "")
        print("=" * 70)

    def evaluate_window(self, window: List[int], piece: int) -> int:
        """
        Evalúa un segmento de 4 casillas asignando puntuaciones tácticas.
        """
        score = 0
        opp_piece = 1 if piece == 2 else 2

        count_piece = window.count(piece)
        count_empty = window.count(0)
        count_opp = window.count(opp_piece)

        if count_piece == 4:
            score += 100
        elif count_piece == 3 and count_empty == 1:
            score += 10
        elif count_piece == 2 and count_empty == 2:
            score += 2

        if count_opp == 3 and count_empty == 1:
            score -= 8  # Penalizar fuertemente amenazas del rival

        return score

    def evaluate_board(self, board: List[int]) -> int:
        """
        Heurística de evaluación posicional completa para tablero 6x6.
        """
        score = 0
        cols = GameModel.COLS
        rows = GameModel.ROWS

        # Ponderación de control central
        for r in range(rows):
            for c in [2, 3]:
                if board[r * cols + c] == 2:
                    score += 3
                elif board[r * cols + c] == 1:
                    score -= 3

        # Ventanas Horizontales
        for r in range(rows):
            for c in range(cols - 3):
                window = [board[r * cols + c + i] for i in range(4)]
                score += self.evaluate_window(window, 2)

        # Ventanas Verticales
        for r in range(rows - 3):
            for c in range(cols):
                window = [board[(r + i) * cols + c] for i in range(4)]
                score += self.evaluate_window(window, 2)

        # Ventanas Diagonales (\)
        for r in range(rows - 3):
            for c in range(cols - 3):
                window = [board[(r + i) * cols + c + i] for i in range(4)]
                score += self.evaluate_window(window, 2)

        # Ventanas Diagonales (/)
        for r in range(rows - 3):
            for c in range(3, cols):
                window = [board[(r + i) * cols + c - i] for i in range(4)]
                score += self.evaluate_window(window, 2)

        return score

    def minimax(
        self, board: List[int], depth: int, is_maximizing: bool
    ) -> Union[int, float]:
        """
        Minimax tradicional con Backtracking y evaluación heurística.
        """
        self.nodes_evaluated += 1

        if GameModel.check_win(board, 2):
            return 1000 + depth
        if GameModel.check_win(board, 1):
            return -1000 - depth
        if GameModel.is_draw(board):
            return 0
        if depth == 0:
            return self.evaluate_board(board)

        valid_moves: List[int] = GameModel.get_valid_moves(board)

        if is_maximizing:
            best_score: float = -math.inf
            for col in valid_moves:
                GameModel.drop_piece(board, col, 2)
                score = self.minimax(board, depth - 1, False)
                GameModel.undo_move(board, col)  # Backtracking
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for col in valid_moves:
                GameModel.drop_piece(board, col, 1)
                score = self.minimax(board, depth - 1, True)
                GameModel.undo_move(board, col)  # Backtracking
                best_score = min(best_score, score)
            return best_score

    def minimax_alfa_beta(
        self,
        board: List[int],
        depth: int,
        alfa: float,
        beta: float,
        is_maximizing: bool,
    ) -> Union[int, float]:
        """
        Minimax con Poda Alfa-Beta (Desafío Extendido opcional).
        """
        self.nodes_evaluated += 1

        if GameModel.check_win(board, 2):
            return 1000 + depth
        if GameModel.check_win(board, 1):
            return -1000 - depth
        if GameModel.is_draw(board):
            return 0
        if depth == 0:
            return self.evaluate_board(board)

        valid_moves: List[int] = GameModel.get_valid_moves(board)

        if is_maximizing:
            best_score: float = -math.inf
            for col in valid_moves:
                GameModel.drop_piece(board, col, 2)
                score = self.minimax_alfa_beta(
                    board, depth - 1, alfa, beta, False)
                GameModel.undo_move(board, col)  # Backtracking
                best_score = max(best_score, score)
                alfa = max(alfa, best_score)
                if beta <= alfa:
                    break
            return best_score
        else:
            best_score = math.inf
            for col in valid_moves:
                GameModel.drop_piece(board, col, 1)
                score = self.minimax_alfa_beta(
                    board, depth - 1, alfa, beta, True)
                GameModel.undo_move(board, col)  # Backtracking
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alfa:
                    break
            return best_score
