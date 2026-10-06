"""
Clase auxiliar Jugada para representar una decisión en el juego 4 en Raya.
Permite que cada movimiento se inserte en el ArbolBinario y se ordene
por su puntuación.
"""

from typing import Any


class Jugada:
    """
    Representa una jugada evaluada en el tablero.

    Atributos:
        puntaje (float): Puntuación o heurística de la jugada.
        columna (int): Columna jugada (0 a 5).
    """

    def __init__(self, puntaje: float, columna: int) -> None:
        self.puntaje: float = float(puntaje)
        self.columna: int = columna

    def __lt__(self, other: Any) -> bool:
        """Criterio de orden menor para el Árbol Binario de Búsqueda."""
        if isinstance(other, Jugada):
            return self.puntaje < other.puntaje
        return self.puntaje < other

    def __le__(self, other: Any) -> bool:
        if isinstance(other, Jugada):
            return self.puntaje <= other.puntaje
        return self.puntaje <= other

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Jugada):
            return self.puntaje > other.puntaje
        return self.puntaje > other

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, Jugada):
            return self.puntaje >= other.puntaje
        return self.puntaje >= other

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Jugada):
            return (self.puntaje == other.puntaje
                    and self.columna == other.columna)
        return False

    def __repr__(self) -> str:
        return f"Jugada(columna={self.columna}, puntaje={self.puntaje})"
