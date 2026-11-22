class Tablero:
    def __init__(self, filas, columnas, obstaculos, cajas, destinos):
        self.filas = filas
        self.columnas = columnas
        self.obstaculos = set(obstaculos)
        self.cajas = set(cajas)
        self.destinos = set(destinos)

    def limite(self, posicion):
        fila, columna = posicion
        return 1 <= fila <= self.filas and 1 <= columna <= self.columnas

    def hay_obstaculo(self, posicion):
        return posicion in self.obstaculos

    def hay_caja(self, posicion):
        return posicion in self.cajas

    def sacar_caja(self, posicion):
        if posicion not in self.cajas:
            raise ValueError(f"No hay caja en {posicion}")
        self.cajas.remove(posicion)

    def colocar_caja(self, posicion):
        if posicion in self.cajas:
            raise ValueError(f"Ya hay caja en esta posición {posicion}")
        self.cajas.add(posicion)

    def comprobar_cajas(self):
        return self.cajas == self.destinos
