from typing import List


class GameModel:
    """
    Representa la lógica y el estado del tablero 4x4 para Conecta 4.

    El tablero se modela como una lista unidimensional de 16 elementos:
    - 0: Casilla vacía.
    - 1: Ficha del Jugador Humano.
    - 2: Ficha del Agente IA.
    """

    @staticmethod
    def get_initial_board() -> List[int]:
        """
        Genera y retorna un tablero nuevo completamente vacío.

        Returns:
            List[int]: Vector de 16 elementos inicializados en 0.
        """
        return [0] * 16

    @staticmethod
    def get_valid_moves(board: List[int]) -> List[int]:
        """
        Obtiene las columnas que todavía tienen espacio para soltar fichas.

        Args:
            board (List[int]): Estado actual del tablero (16 posiciones).

        Returns:
            List[int]: Lista de índices de columna válidos (0 a 3).
        """
        return [col for col in range(4) if board[col] == 0]

    @staticmethod
    def drop_piece(board: List[int], col: int, player: int) -> bool:
        """
        Aplica gravedad y coloca una ficha en la fila libre más baja.

        Args:
            board (List[int]): Estado actual del tablero.
            col (int): Índice de columna elegida (0 a 3).
            player (int): Identificador del jugador (1: Humano, 2: IA).

        Returns:
            bool: True si la ficha fue insertada, False si la columna está llena.
        """
        for row in range(3, -1, -1):
            idx = row * 4 + col
            if board[idx] == 0:
                board[idx] = player
                return True
        return False

    @staticmethod
    def undo_move(board: List[int], col: int) -> None:
        """
        Retira la ficha superior de una columna para operaciones de Backtracking.

        Args:
            board (List[int]): Estado actual del tablero.
            col (int): Índice de columna donde se revertirá el último movimiento.

        Returns:
            None
        """
        for row in range(4):
            idx = row * 4 + col
            if board[idx] != 0:
                board[idx] = 0
                return

    @staticmethod
    def check_win(board: List[int], player: int) -> bool:
        """
        Comprueba si un jugador ha conectado 4 fichas consecutivas.

        Args:
            board (List[int]): Estado actual del tablero.
            player (int): Identificador del jugador (1 o 2).

        Returns:
            bool: True si el jugador tiene 4 en raya, False en caso contrario.
        """
        # Comprobación de Filas
        for r in range(4):
            if all(board[r * 4 + c] == player for c in range(4)):
                return True

        # Comprobación de Columnas
        for c in range(4):
            if all(board[r * 4 + c] == player for r in range(4)):
                return True

        # Comprobación de Diagonal principal (\)
        if all(board[i * 4 + i] == player for i in range(4)):
            return True

        # Comprobación de Diagonal secundaria (/)
        if all(board[i * 4 + (3 - i)] == player for i in range(4)):
            return True

        return False

    @staticmethod
    def is_draw(board: List[int]) -> bool:
        """
        Verifica si la partida ha finalizado en empate (tablero lleno sin victoria).

        Args:
            board (List[int]): Estado actual del tablero.

        Returns:
            bool: True si no quedan casillas vacías, False en caso contrario.
        """
        return 0 not in board
