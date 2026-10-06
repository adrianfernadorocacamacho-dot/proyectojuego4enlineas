from collections import deque

try:
    from ClaseNodo import ClaseNodo
except ImportError:
    from .ClaseNodo import ClaseNodo


class ArbolBinario:

    def __init__(self):
        self._raiz = None

    '''
    nota:inserta un nuevo valor en el árbol binario de búsqueda.
    argumentos: recibe un numero entero o dato comparable
    retorna: nada, pero actualiza la raíz del árbol. 
    '''

    def insertar(self, valor):
        self._raiz = self._insertarRecursivo(self._raiz, valor)

    '''
    nota: función auxiliar recursiva que busca la posición correcta
          e inserta el nuevo valor dentro del árbol binario de búsqueda.
    argumentos: 
        - raizAux: nodo actual (puede ser None si llegamos a un lugar vacío).
        - valor: dato que se quiere insertar.
    retorna: 
        - un objeto ClaseNodo que representa la raíz del subárbol modificado.
    '''

    def _insertarRecursivo(self, raizAux, valor):
        # Caso Base
        if raizAux is None:
            raizAux = ClaseNodo(valor)
            return raizAux
        else:
            if valor < raizAux.getValor():
                raizAux.setHijoIzquierdo(self._insertarRecursivo(raizAux.getHijoIzquierdo(), valor))
            else:
                raizAux.setHijoDerecho(self._insertarRecursivo(raizAux.getHijoDerecho(), valor))
            return raizAux

    """
    Nota:Inserta un nuevo nodo en el árbol binario de forma iterativa.
    Argumentos:
        valor: El valor que se desea insertar en el árbol.
    Retorna:
        None.
    """
    def insertarIterativo(self, valor):
        nuevoNodo = ClaseNodo(valor)
        if self._raiz is None:
            self._raiz = nuevoNodo
            return
        nodoActual = self._raiz
        while True:
            if valor < nodoActual.getValor():
                if nodoActual.getHijoIzquierdo() is None:
                    nodoActual.setHijoIzquierdo(nuevoNodo)
                    return
                nodoActual = nodoActual.getHijoIzquierdo()
            else:
                if nodoActual.getHijoDerecho() is None:
                    nodoActual.setHijoDerecho(nuevoNodo)
                    return
                nodoActual = nodoActual.getHijoDerecho()

    '''
    nota: verifica si el árbol está vacío.
    argumentos: ninguno.
    retorna: True si la raíz es None (árbol vacío), False en caso contrario.
    '''
    def isVacio(self):
        return self._raiz is None

    '''
    nota: determina si un nodo es hoja (no tiene hijos).
    argumentos: 
        - nodo: objeto de tipo ClaseNodo.
    retorna: True si el nodo no tiene hijos izquierdo ni derecho,
             False en caso contrario.
    '''
    def esHoja(self, nodo):
        return nodo.getHijoIzquierdo() is None and nodo.getHijoDerecho() is None

    """
    Nota:Busca un valor en el árbol binario de búsqueda.
    Argumentos:
        valor: El valor que se desea buscar en el árbol.
    Retorna:
        bool: True si el valor se encuentra en el árbol, False en caso contrario.
    """
    def buscar(self, valor):
        return self._buscarRecursivo(self._raiz, valor)

    """
    Nota:Función auxiliar recursiva para realizar la búsqueda en el árbol.
    Argumentos:
        nodo (ClaseNodo | None): El nodo actual del árbol desde donde se realiza la búsqueda.
        valor: El valor que se desea buscar.
    Retorna:
        bool: True si el valor está en el subárbol a partir del nodo dado,
              False si no se encuentra.
    """
    def _buscarRecursivo(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.getValor() == valor:
            return True
        elif valor < nodo.getValor():
            return self._buscarRecursivo(nodo.getHijoIzquierdo(), valor)
        else:
            return self._buscarRecursivo(nodo.getHijoDerecho(), valor)

    """
    Nota:Busca un valor en el árbol binario de búsqueda de forma iterativa.
    Argumentos:
        valor: El valor que se desea buscar en el árbol.
    Retorna:
        bool: True si el valor se encuentra en el árbol, False en caso contrario.
    """
    def buscarIterativo(self, valor):
        nodoActual = self._raiz
        while nodoActual is not None:
            if nodoActual.getValor() == valor:
                return True
            elif valor < nodoActual.getValor():
                nodoActual = nodoActual.getHijoIzquierdo()
            else:
                nodoActual = nodoActual.getHijoDerecho()
        return False

    """
    nota:Recorre el árbol binario de búsqueda en orden (in-order) de manera iterativa.
    Retorna:
        list: Una lista con los valores del árbol en orden ascendente.
    """
    def inOrden(self):
        listado = []
        pila = []
        nodoActual = self._raiz

        while nodoActual is not None or pila:
            while nodoActual is not None:
                pila.append(nodoActual)
                nodoActual = nodoActual.getHijoIzquierdo()

            nodoActual = pila.pop()
            listado.append(nodoActual.getValor())
            nodoActual = nodoActual.getHijoDerecho()

        return listado

    """
    Recorre el árbol binario de búsqueda en orden (in-order) de manera recursiva.
    Retorna:
        list: Una lista con los valores del árbol en orden ascendente.
    """
    def inOrdenRecursivo(self):
        listado = []
        self._inOrdenRecursivoAux(self._raiz, listado)
        return listado

    """
    Función auxiliar recursiva para recorrer el árbol en orden.
    Argumentos:
        nodo (ClaseNodo | None): Nodo actual del recorrido.
        listado (list): Lista en la que se almacenan los valores recorridos.
    """
    def _inOrdenRecursivoAux(self, nodo, listado):
        if nodo is not None:
            self._inOrdenRecursivoAux(nodo.getHijoIzquierdo(), listado)
            listado.append(nodo.getValor())
            self._inOrdenRecursivoAux(nodo.getHijoDerecho(), listado)

    """
    Recorre el árbol binario de búsqueda en postorden (post-order) de manera iterativa.
    Retorna:
        list: Una lista con los valores del árbol en orden postorden.
    """
    def posOrden(self):
        listado = []
        if self._raiz is None:
            return listado

        pila1 = [self._raiz]
        pila2 = []

        while pila1:
            nodo = pila1.pop()
            pila2.append(nodo)

            if nodo.getHijoIzquierdo() is not None:
                pila1.append(nodo.getHijoIzquierdo())
            if nodo.getHijoDerecho() is not None:
                pila1.append(nodo.getHijoDerecho())

        while pila2:
            listado.append(pila2.pop().getValor())

        return listado

    """
    Recorre el árbol binario de búsqueda en postorden (post-order) de manera recursiva.
    Retorna:
        list: Una lista con los valores del árbol en orden postorden.
    """
    def posOrdenRecursivo(self):
        listado = []
        self._posOrdenRecursivoAux(self._raiz, listado)
        return listado

    """
    Función auxiliar recursiva para recorrer el árbol en postorden.
    """
    def _posOrdenRecursivoAux(self, nodo, listado):
        if nodo is not None:
            self._posOrdenRecursivoAux(nodo.getHijoIzquierdo(), listado)
            self._posOrdenRecursivoAux(nodo.getHijoDerecho(), listado)
            listado.append(nodo.getValor())

    """
    Recorre el árbol binario de búsqueda en preorden (pre-order) de manera iterativa.
    Retorna:
        list: Una lista con los valores del árbol en orden preorden.
    """
    def preOrden(self):
        listado = []
        if self._raiz is None:
            return listado

        pila = [self._raiz]

        while pila:
            nodo = pila.pop()
            listado.append(nodo.getValor())

            if nodo.getHijoDerecho() is not None:
                pila.append(nodo.getHijoDerecho())
            if nodo.getHijoIzquierdo() is not None:
                pila.append(nodo.getHijoIzquierdo())

        return listado

    """
    Recorre el árbol binario de búsqueda en preorden (pre-order) de manera recursiva.
    Retorna:
        list: Una lista con los valores del árbol en orden preorden.
    """
    def preOrdenRecursivo(self):
        listado = []
        self._preOrdenRecursivoAux(self._raiz, listado)
        return listado

    """
    Función auxiliar recursiva para recorrer el árbol en preorden.
    """
    def _preOrdenRecursivoAux(self, nodo, listado):
        if nodo is not None:
            listado.append(nodo.getValor())
            self._preOrdenRecursivoAux(nodo.getHijoIzquierdo(), listado)
            self._preOrdenRecursivoAux(nodo.getHijoDerecho(), listado)

    """
    Calcula la altura del árbol binario de búsqueda de manera recursiva.
    Retorna: (int) La altura del árbol.
    """
    def altura(self):
        return self._alturaAux(self._raiz)

    """
    Función auxiliar recursiva para calcular la altura del árbol.
    """
    def _alturaAux(self, nodo):
        if nodo is None:
            return 0
        altura_izquierda = self._alturaAux(nodo.getHijoIzquierdo())
        altura_derecha = self._alturaAux(nodo.getHijoDerecho())
        return 1 + max(altura_izquierda, altura_derecha)

    """
    Función iterativa para contar altura
    """
    def alturaIt(self):
        alturaDelArbol = 0
        if not self.isVacio():
            cola = deque([self._raiz])
            while cola:
                cantNodosEnLaCola = len(cola)
                for _ in range(cantNodosEnLaCola):
                    nodoAux = cola.popleft()
                    if nodoAux.getHijoIzquierdo() is not None:
                        cola.append(nodoAux.getHijoIzquierdo())
                    if nodoAux.getHijoDerecho() is not None:
                        cola.append(nodoAux.getHijoDerecho())
                alturaDelArbol += 1
        return alturaDelArbol

    """
    Función recursiva para contar nodos
    Retorna: (int) La cantidad de nodos en el árbol.
    """
    def cantidadNodos(self):
        return self._cantidadNodosAux(self._raiz)

    """
    Función auxiliar recursiva para contar nodos
    """
    def _cantidadNodosAux(self, nodo):
        if nodo is None:
            return 0
        cantidad_izquierda = self._cantidadNodosAux(nodo.getHijoIzquierdo())
        cantidad_derecha = self._cantidadNodosAux(nodo.getHijoDerecho())
        return 1 + cantidad_izquierda + cantidad_derecha

    """
    Función iterativa para contar nodos
    """
    def cantidadNodosIt(self):
        if self.isVacio():
            return 0
        cantidad = 0
        cola = deque([self._raiz])
        while cola:
            nodo = cola.popleft()
            cantidad += 1
            if nodo.getHijoIzquierdo() is not None:
                cola.append(nodo.getHijoIzquierdo())
            if nodo.getHijoDerecho() is not None:
                cola.append(nodo.getHijoDerecho())
        return cantidad

    """
    Realiza un recorrido por amplitud (nivel por nivel) del árbol binario.
    Retorna: (list) Los valores de los nodos en el orden en que fueron visitados.
    """
    def amplitud(self):
        if self.isVacio():
            return []

        resultado = []
        cola = deque([self._raiz])

        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.getValor())

            if nodo.getHijoIzquierdo() is not None:
                cola.append(nodo.getHijoIzquierdo())
            if nodo.getHijoDerecho() is not None:
                cola.append(nodo.getHijoDerecho())

        return resultado

    """
    Recorrido por niveles recursivo
    """
    def amplitudRecursivo(self):
        resultado = []
        h = self.altura()

        for nivel in range(1, h + 1):
            self._amplitudRecursivoAux(self._raiz, nivel, resultado)

        return resultado

    def _amplitudRecursivoAux(self, nodo, nivel, resultado):
        if nodo is None:
            return
        if nivel == 1:
            resultado.append(nodo.getValor())
        elif nivel > 1:
            self._amplitudRecursivoAux(nodo.getHijoIzquierdo(), nivel - 1, resultado)
            self._amplitudRecursivoAux(nodo.getHijoDerecho(), nivel - 1, resultado)

    """
    Elimina un valor del árbol binario de búsqueda.
    """
    def eliminar(self, valor):
        self._raiz = self._eliminarRecursivo(self._raiz, valor)

    def _eliminarRecursivo(self, nodo, valor):
        if nodo is None:
            return None

        if valor < nodo.getValor():
            nodo.setHijoIzquierdo(self._eliminarRecursivo(nodo.getHijoIzquierdo(), valor))
        elif valor > nodo.getValor():
            nodo.setHijoDerecho(self._eliminarRecursivo(nodo.getHijoDerecho(), valor))
        else:
            if nodo.getHijoIzquierdo() is None and nodo.getHijoDerecho() is None:
                return None
            elif nodo.getHijoIzquierdo() is None:
                return nodo.getHijoDerecho()
            elif nodo.getHijoDerecho() is None:
                return nodo.getHijoIzquierdo()
            else:
                sucesor = self._minValorNodo(nodo.getHijoDerecho())
                nodo.setValor(sucesor.getValor())
                nodo.setHijoDerecho(self._eliminarRecursivo(nodo.getHijoDerecho(), sucesor.getValor()))

        return nodo

    def _minValorNodo(self, nodo):
        actual = nodo
        while actual.getHijoIzquierdo() is not None:
            actual = actual.getHijoIzquierdo()
        return actual

    def getRaiz(self):
        return self._raiz

    def limpiarArbol(self):
        """Limpiar todo el árbol"""
        self._raiz = None

    def obtenerMayor(self):
        """Encuentra el valor máximo en el árbol binario de búsqueda."""
        if self.isVacio():
            return None
        actual = self._raiz
        while actual.getHijoDerecho() is not None:
            actual = actual.getHijoDerecho()
        return actual.getValor()

    def obtenerEstructuraVisual(self):
        """Obtener una representación visual simple del árbol"""
        if self.isVacio():
            return "Árbol vacío"
        return self._estructuraVisualRecursiva(self._raiz, "", True)

    def _estructuraVisualRecursiva(self, nodo, prefijo, esUltimo):
        if nodo is None:
            return ""

        resultado = prefijo + ("└── " if esUltimo else "├── ") + str(nodo.getValor()) + "\n"

        hijos = []
        if nodo.getHijoIzquierdo() is not None:
            hijos.append(("izq", nodo.getHijoIzquierdo()))
        if nodo.getHijoDerecho() is not None:
            hijos.append(("der", nodo.getHijoDerecho()))

        for i, (tipo, hijo) in enumerate(hijos):
            esUltimoHijo = i == len(hijos) - 1
            nuevoPrefijo = prefijo + ("    " if esUltimo else "│   ")
            resultado += self._estructuraVisualRecursiva(hijo, nuevoPrefijo, esUltimoHijo)

        return resultado
