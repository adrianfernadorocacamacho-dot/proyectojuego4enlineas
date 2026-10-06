from typing import List


class GameModel:
    """
    Representa la lógica y el estado del tablero 6x6 para Conecta 4.

    El tablero se modela como una lista unidimensional de 36 casillas
    (6 filas x 6 columnas):
    - 0: Casilla vacía.
    - 1: Ficha del Jugador Humano (Rojo).
    - 2: Ficha del Agente IA (Amarillo).
    """

    ROWS: int = 6
    COLS: int = 6
    BOARD_SIZE: int = 36
    WIN_STREAK: int = 4

    @staticmethod
    def get_initial_board() -> List[int]:
        """
        Genera y retorna un tablero nuevo 6x6 completamente vacío.

        Returns:
            List[int]: Vector de 36 elementos inicializados en 0.
        """
        return [0] * GameModel.BOARD_SIZE

    @staticmethod
    def get_valid_moves(board: List[int]) -> List[int]:
        """
        Obtiene las columnas que todavía tienen espacio para soltar fichas.

        Args:
            board (List[int]): Estado actual del tablero (36 casillas).

        Returns:
            List[int]: Lista de índices de columna válidos (0 a 5).
        """
        return [col for col in range(GameModel.COLS) if board[col] == 0]

    @staticmethod
    def drop_piece(board: List[int], col: int, player: int) -> bool:
        """
        Aplica gravedad y coloca una ficha en la fila libre más baja.

        Args:
            board (List[int]): Estado actual del tablero (36 casillas).
            col (int): Índice de columna elegida (0 a 5).
            player (int): Identificador del jugador (1: Humano, 2: IA).

        Returns:
            bool: True si la ficha fue insertada, False si está llena.
        """
        if col < 0 or col >= GameModel.COLS:
            return False

        for row in range(GameModel.ROWS - 1, -1, -1):
            idx = row * GameModel.COLS + col
            if board[idx] == 0:
                board[idx] = player
                return True
        return False

    @staticmethod
    def undo_move(board: List[int], col: int) -> None:
        """
        Retira la ficha superior de una columna para Backtracking.

        Args:
            board (List[int]): Estado actual del tablero.
            col (int): Índice de columna donde revertir la última ficha.
        """
        for row in range(GameModel.ROWS):
            idx = row * GameModel.COLS + col
            if board[idx] != 0:
                board[idx] = 0
                return

    @staticmethod
    def check_win(board: List[int], player: int) -> bool:
        """
        Comprueba si un jugador ha conectado 4 fichas consecutivas (6x6)
        en horizontal, vertical o cualquiera de las dos diagonales.

        Args:
            board (List[int]): Estado actual del tablero (36 posiciones).
            player (int): Identificador del jugador (1 o 2).

        Returns:
            bool: True si el jugador tiene 4 en línea, False en caso contrario.
        """
        cols = GameModel.COLS  # 6
        rows = GameModel.ROWS  # 6

        # 1. Comprobación Horizontal (4 en fila)
        for r in range(rows):
            for c in range(cols - 3):  # c de 0 a 2
                if all(board[r * cols + c + i] == player for i in range(4)):
                    return True

        # 2. Comprobación Vertical (4 en columna)
        for r in range(rows - 3):  # r de 0 a 2
            for c in range(cols):
                if all(board[(r + i) * cols + c] == player for i in range(4)):
                    return True

        # 3. Comprobación Diagonal Principal (\ descendente)
        for r in range(rows - 3):  # r de 0 a 2
            for c in range(cols - 3):  # c de 0 a 2
                if all(board[(r + i) * cols + (c + i)] == player
                       for i in range(4)):
                    return True

        # 4. Comprobación Diagonal Secundaria (/ ascendente)
        for r in range(rows - 3):  # r de 0 a 2
            for c in range(3, cols):  # c de 3 a 5
                if all(board[(r + i) * cols + (c - i)] == player
                       for i in range(4)):
                    return True

        return False

    @staticmethod
    def is_draw(board: List[int]) -> bool:
        """
        Verifica si la partida ha finalizado en empate (tablero lleno).

        Args:
            board (List[int]): Estado actual del tablero (36 posiciones).

        Returns:
            bool: True si no quedan casillas vacías (0), False si aún hay.
        """
        return 0 not in board
