"""
Módulo de modelos y agentes para el juego Conecta 4 (4x4).

Contiene:
- GameModel: Tablero y lógica de Connect 4.
- MinimaxAgent: Agente inteligente que utiliza ArbolBinario y ClaseNodo.
- ArbolBinario y ClaseNodo: Estructuras clásicas de árbol binario de búsqueda.
- run_benchmark: Prueba comparativa de rendimiento.
"""

from .game_model import GameModel
from .minimax_agent import MinimaxAgent
from .tree import ArbolBinario, ClaseNodo, Arbol, Nodo, Jugada
from .benchmark import run_benchmark

__all__ = [
    "GameModel",
    "MinimaxAgent",
    "ArbolBinario",
    "ClaseNodo",
    "Arbol",
    "Nodo",
    "Jugada",
    "run_benchmark",
]
