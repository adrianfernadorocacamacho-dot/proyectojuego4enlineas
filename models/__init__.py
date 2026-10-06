"""
Módulo de modelos y agentes para el juego Conecta 4 (6x6).

Contiene:
- GameModel: Tablero y lógica de Connect 4.
- MinimaxAgent: Agente inteligente que utiliza ArbolBinario y ClaseNodo.
- MLAgent: Agente ML entrenado con DecisionTreeClassifier (scikit-learn).
- ArbolBinario y ClaseNodo: Estructuras clásicas de árbol binario.
- run_benchmark: Generador de métricas comparativas.
"""

from .game_model import GameModel
from .minimax_agent import MinimaxAgent
from .ml_agent import MLAgent
from .tree import ArbolBinario, ClaseNodo, Arbol, Nodo, Jugada
from .benchmark import run_benchmark

__all__ = [
    "GameModel",
    "MinimaxAgent",
    "MLAgent",
    "ArbolBinario",
    "ClaseNodo",
    "Arbol",
    "Nodo",
    "Jugada",
    "run_benchmark",
]
