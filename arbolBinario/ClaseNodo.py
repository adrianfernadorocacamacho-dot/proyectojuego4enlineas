'''
title: clase nodo
autor: Denilson Ariel Cruz Huarachi
creado: 24-08-2025
version: 3.13.7
'''


class ClaseNodo:

    '''
    nota: representa un nodo de un árbol binario.
    argumentos:
        - valor: número o dato que se almacenará en el nodo.
    retorna: un objeto de tipo ClaseNodo con valor y referencias
             a hijo izquierdo y derecho inicializadas en None.
    '''

    def __init__(self, valor):
        self._valor = valor
        self._hijoIzquierdo = None
        self._hijoDerecho = None

    '''
    nota: obtiene el hijo izquierdo del nodo.
    argumentos: ninguno.
    retorna: el objeto ClaseNodo que es hijo izquierdo, o None si no existe.
    '''

    def getHijoIzquierdo(self):
        return self._hijoIzquierdo

    '''
    nota: obtiene el hijo derecho del nodo.
    argumentos: ninguno.
    retorna: el objeto ClaseNodo que es hijo derecho, o None si no existe.
    '''

    def getHijoDerecho(self):
        return self._hijoDerecho

    '''
    nota: asigna un nodo como hijo izquierdo.
    argumentos:
        - nodo: objeto de tipo ClaseNodo a establecer como hijo izquierdo.
    retorna: nada.
    '''

    def setHijoIzquierdo(self, nodo):
        self._hijoIzquierdo = nodo

    '''
    nota: asigna un nodo como hijo derecho.
    argumentos:
        - nodo: objeto de tipo ClaseNodo a establecer como hijo derecho.
    retorna: nada.
    '''

    def setHijoDerecho(self, nodo):
        self._hijoDerecho = nodo

    '''
    nota: obtiene el valor almacenado en el nodo.
    argumentos: ninguno.
    retorna: el valor del nodo.
    '''

    def getValor(self):
        return self._valor

    '''
    nota: asigna un nuevo valor al nodo.
    argumentos:
        - valor: dato que se quiere almacenar en el nodo.
    retorna: nada.
    '''

    def setValor(self, valor):
        self._valor = valor
