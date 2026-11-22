class Pila:
    def __init__(self, fondo="Z0"):
        self.fondo = fondo
        self.elementos = [fondo]
        self.cantidad_pila = 0

    def tope(self):
        return self.elementos[-1]

    def agregar(self, simbolo):
        self.elementos.append(simbolo)
        self.cantidad_pila = max(self.cantidad_pila, len(self.elementos) - 1)

    def sacar(self):
        return self.elementos.pop()

    def pila_vacia(self):
        return len(self.elementos) == 1 and self.elementos[0] == self.fondo

    def mostrar_pila(self):
        return " ".join(reversed(self.elementos))
