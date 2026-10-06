"""
Módulo puente para compatibilidad. Re-exporta la estructura de datos tradicional
de la carpeta arbolBinario (ClaseNodo y ArbolBinario).
"""

from arbolBinario.ClaseNodo import ClaseNodo
from arbolBinario.ClaseArbolBinario import ArbolBinario
from arbolBinario.Jugada import Jugada

# Alias para facilitar uso indistinto
Nodo = ClaseNodo
Arbol = ArbolBinario

__all__ = ["ClaseNodo", "ArbolBinario", "Nodo", "Arbol", "Jugada"]
