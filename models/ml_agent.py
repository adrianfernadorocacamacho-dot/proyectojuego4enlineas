import os
import pickle
import random
from typing import List, Optional, Tuple

from sklearn.tree import DecisionTreeClassifier

from .game_model import GameModel


class MLAgent:
    """
    Agente basado en Machine Learning utilizando Árbol de Decisión.

    Genera un dataset sintético jugando partidas automáticas para predecir
    el mejor movimiento legal en tiempo O(1).

    Atributos:
        model_path (str): Ruta en disco hacia el archivo serializado (.pkl).
        model (Optional[DecisionTreeClassifier]): Modelo de clasificación de
            Scikit-Learn.
    """

    def __init__(self, model_path: str = "models/connect4_dt_model.pkl") -> None:
        """
        Inicializa el agente cargando o entrenando el modelo en disco.

        Args:
            model_path (str, optional): Ruta donde persistir el modelo.
                Por defecto 'models/connect4_dt_model.pkl'.

        Returns:
            None
        """
        self.model_path: str = model_path
        self.model: Optional[DecisionTreeClassifier] = None
        self.load_or_train()

    def generate_data(
        self, num_games: int = 1000
    ) -> Tuple[List[List[int]], List[int]]:
        """
        Simula partidas automáticas para recopilar características y etiquetas.

        Args:
            num_games (int, optional): Cantidad de partidas sintéticas a simular.
                Por defecto 1000.

        Returns:
            Tuple[List[List[int]], List[int]]: Tupla (X, y) donde X contiene
            los estados del tablero y y las columnas que llevaron a victorias.
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
                move: int = random.choice(moves)

                if turn == 2:
                    history.append((list(board), move))

                GameModel.drop_piece(board, move, turn)
                if GameModel.check_win(board, turn):
                    if turn == 2:
                        for b, m in history:
                            X.append(b)
                            y.append(m)
                    break
                turn = 3 - turn

        return X, y

    def train_model(self) -> None:
        """
        Entrena un nuevo árbol de decisión (DecisionTreeClassifier) y lo guarda.

        Returns:
            None
        """
        print("Generando dataset sintético (1000+ partidas)...")
        X, y = self.generate_data(3000)

        if not X:
            # Fallback en caso de que ninguna partida terminara en victoria
            X = [[0] * 16]
            y = [0]

        print("Entrenando DecisionTreeClassifier...")
        self.model = DecisionTreeClassifier(max_depth=10)
        self.model.fit(X, y)

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)
        print(f"Modelo guardado en {self.model_path}")

    def load_or_train(self) -> None:
        """
        Carga el modelo serializado si existe; si no, ejecuta el entrenamiento.

        Returns:
            None
        """
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
            except Exception:
                self.train_model()
        else:
            self.train_model()

    def get_move(self, board: List[int]) -> Tuple[Optional[int], int]:
        """
        Predice la columna óptima a jugar utilizando el árbol de decisión entrenado.

        Args:
            board (List[int]): Estado actual del tablero (16 posiciones).

        Returns:
            Tuple[Optional[int], int]: Tupla con la columna elegida (o None si no
            hay opciones) y 1 representando el coste de inferencia O(1).
        """
        valid_moves: List[int] = GameModel.get_valid_moves(board)
        if not valid_moves:
            return None, 1

        if self.model is None:
            return random.choice(valid_moves), 1

        pred: int = int(self.model.predict([board])[0])

        # Validar si el movimiento sugerido por la red/árbol es legal
        if pred in valid_moves:
            return pred, 1

        return random.choice(valid_moves), 1
