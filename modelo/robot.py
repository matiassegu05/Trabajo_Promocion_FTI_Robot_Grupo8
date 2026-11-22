class Robot:
    Movimientos = {
        "arriba": (-1, 0),
        "abajo": (1, 0),
        "izquierda": (0, -1),
        "derecha": (0, 1),
    }

    def __init__(self, posicion_inicial):
        self.posicion_inicial = posicion_inicial
        self.posicion_actual = posicion_inicial
        self.con_carga = False

    def ejecutar_accion(self, accion, tablero):
        if accion in self.Movimientos:
            movimiento_fila, movimiento_columna = self.Movimientos[accion]
            nueva_posicion = (
                self.posicion_actual[0] + movimiento_fila,
                self.posicion_actual[1] + movimiento_columna,
            )

            if not tablero.limite(nueva_posicion):
                raise ValueError(f"Fuera de los límites {nueva_posicion}")
            if tablero.hay_obstaculo(nueva_posicion):
                raise ValueError(f"Hay un obstáculo en {nueva_posicion}")

            self.posicion_actual = nueva_posicion

        elif accion == "agarrar":
            if self.con_carga:
                raise ValueError("La pinza ya está ocupada")
            tablero.sacar_caja(self.posicion_actual)
            self.con_carga = True

        elif accion == "soltar":
            if not self.con_carga:
                raise ValueError("No tiene nada en la pinza")
            tablero.colocar_caja(self.posicion_actual)
            self.con_carga = False

        elif accion in ("viaje", "finviaje"):
            pass

        else:
            raise ValueError(f"Acción incorrecta: {accion}")
