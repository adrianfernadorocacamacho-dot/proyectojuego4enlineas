"""
Clase auxiliar Jugada para representar una decisión en el juego 4 en Raya.
Permite que cada movimiento se inserte en el ArbolBinario y se ordene
automáticamente por su puntuación mediante los operadores de comparación.
"""

from typing import Any


class Jugada:
    """
    Representa una jugada evaluada en el tablero.

    Atributos:
        puntaje (float): Puntuación o heurística de la jugada.
        columna (int): Columna jugada (0 a 3).
    """

    def __init__(self, puntaje: float, columna: int) -> None:
        self.puntaje: float = float(puntaje)
        self.columna: int = columna

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Jugada):
            if self.puntaje != other.puntaje:
                return self.puntaje < other.puntaje
            return self.columna < other.columna
        return self.puntaje < other

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Jugada):
            if self.puntaje != other.puntaje:
                return self.puntaje > other.puntaje
            return self.columna > other.columna
        return self.puntaje > other

    def __le__(self, other: Any) -> bool:
        return self < other or self == other

    def __ge__(self, other: Any) -> bool:
        return self > other or self == other

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Jugada):
            return self.puntaje == other.puntaje and self.columna == other.columna
        return self.puntaje == other

    def __str__(self) -> str:
        return f"Columna {self.columna} (Puntaje: {self.puntaje})"

    def __repr__(self) -> str:
        return f"Jugada(columna={self.columna}, puntaje={self.puntaje})"
