"""
Módulo del Agente de Machine Learning (DecisionTreeClassifier).

Cumple los requerimientos de:
1. Generación de dataset válido mediante simulaciones automáticas en 6x6.
2. Entrenamiento de DecisionTreeClassifier de scikit-learn.
3. Visualización y exportación de las reglas del árbol de decisión.
"""

import os
import pickle
import random
from typing import List, Optional, Tuple

from sklearn.tree import DecisionTreeClassifier, export_text

from .game_model import GameModel


class MLAgent:
    """
    Agente de Machine Learning con Árbol de Decisión.

    Atributos:
        model_path (str): Ruta hacia el modelo serializado (.pkl).
        model (Optional[DecisionTreeClassifier]): Instancia del clasificador.
    """

    def __init__(
        self, model_path: str = "models/connect4_dt_model.pkl"
    ) -> None:
        self.model_path: str = model_path
        self.model: Optional[DecisionTreeClassifier] = None
        self.load_or_train()

    def generate_data(
        self, num_games: int = 1500
    ) -> Tuple[List[List[int]], List[int]]:
        """
        Genera dataset sintético mediante simulaciones en el tablero 6x6.
        Recopila los estados y columnas ganadoras de la IA.

        Args:
            num_games (int, optional): Número de partidas a simular.

        Returns:
            Tuple[List[List[int]], List[int]]: Tupla (X, y) donde:
                - X: Lista de tableros (36 casillas).
                - y: Columnas ganadoras (0 a 5).
        """
        X: List[List[int]] = []
        y: List[int] = []

        for _ in range(num_games):
            board: List[int] = GameModel.get_initial_board()
            history: List[Tuple[List[int], int]] = []
            turn: int = 1

            while True:
                moves: List[int] = GameModel.get_valid_moves(board)
                if not moves:
                    break

                col: int = random.choice(moves)

                # Si es el turno de la IA (2), registrar estado previo
                if turn == 2:
                    history.append((list(board), col))

                GameModel.drop_piece(board, col, turn)

                # Si la IA gana, guardar historial de jugadas
                if GameModel.check_win(board, turn):
                    if turn == 2:
                        for b, m in history:
                            X.append(b)
                            y.append(m)
                    break

                # Alternar turno (1 <-> 2)
                turn = 3 - turn

        return X, y

    def train_model(self, num_games: int = 1500) -> None:
        """
        Entrena un nuevo DecisionTreeClassifier y lo guarda en disco.
        """
        print(f"Simulando {num_games} partidas en tablero 6x6...")
        X, y = self.generate_data(num_games)

        if not X:
            X = [[0] * GameModel.BOARD_SIZE]
            y = [0]

        print(f"Dataset generado: {len(X)} muestras. Entrenando árbol...")
        self.model = DecisionTreeClassifier(max_depth=10, random_state=42)
        self.model.fit(X, y)

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)
        print(f"Modelo guardado exitosamente en: {self.model_path}")

    def load_or_train(self) -> None:
        """
        Carga el modelo serializado (.pkl) o ejecuta entrenamiento.
        """
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
            except Exception:
                self.train_model()
        else:
            self.train_model()

    def get_move(self, board: List[int]) -> Optional[int]:
        """
        Predice la columna óptima en tiempo O(1) con el Árbol entrenado.

        Args:
            board (List[int]): Tablero actual de 36 posiciones.

        Returns:
            Optional[int]: Columna predicha (0 a 5) o jugada válida.
        """
        valid_moves: List[int] = GameModel.get_valid_moves(board)
        if not valid_moves:
            return None

        if self.model is None:
            return random.choice(valid_moves)

        pred: int = int(self.model.predict([board])[0])

        # Verificar que la columna predicha sea legal
        if pred in valid_moves:
            return pred

        return random.choice(valid_moves)

    def get_rules_text(self, max_depth: int = 4) -> str:
        """
        Visualización de reglas del DecisionTreeClassifier (rúbrica).

        Args:
            max_depth (int, optional): Profundidad de reglas. Por defecto 4.

        Returns:
            str: Reglas aprendidas en texto.
        """
        if self.model is None:
            return "El modelo aún no está entrenado."

        feature_names = [f"Casilla_{i}" for i in range(GameModel.BOARD_SIZE)]
        return export_text(
            self.model,
            feature_names=feature_names,
            max_depth=max_depth,
        )
