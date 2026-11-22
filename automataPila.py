from pila import Pila

class AutomataPila:
    alfabeto ={"arriba", "abajo", "izquierda", "derecha", "agarrar", "soltar", "viaje", "finviaje"}

    inverso ={
        "arriba": "abajo",
        "abajo": "arriba",
        "izquierda": "derecha",
        "derecha": "izquierda",
    }

    traduccion = {
        "arriba": "ARR",
        "abajo": "AB",
        "izquierda": "IZ",
        "derecha": "DR",
    }
    destraduccion = {codigo: orden for orden, codigo in traduccion.items()}

    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.estado = "q0"
        self.pila = Pila("Z0")

    def transicion(self, accion):
        tope = self.pila.tope()

        match (self.estado, accion):
            case ("q0" | "q_funcionando", m) if m in self.inverso: 
                return
            case ("q0" | "q_funcionando", "viaje"):
                self.estado = "q_moviendose"
            case ("q_moviendose", m) if m in self.inverso:
                self.pila.agregar(self.traduccion[self.inverso[m]])
            case ("q_moviendose", "agarrar"):
                self.estado = "q_volviendo"
            case ("q_volviendo", m) if m in self.inverso and self.destraduccion.get(tope) == m:
                orden_sacada = self.destraduccion[self.pila.sacar()]
            case ("q_volviendo", "soltar") if tope == "Z0":
                self.estado = "q_terminado"
            case ("q_terminado", "finviaje") if tope == "Z0":
                self.estado = "q_funcionando"
            case _:
                raise ValueError(f"Se rechaza {accion}, queda en estado= {self.estado} y tope={tope}")

    def paso(self, accion, recorrido):
        self.transicion(accion)
        recorrido.append((len(recorrido) + 1, accion, self.estado, self.pila.mostrar_pila()))

    def validar(self, cadena):
        self.reiniciar()
        tokens = cadena.split()

        if not tokens:
            raise ValueError("Error: la cadena esta vacia") 
        for indice, accion in enumerate(tokens, start=1):
            if accion not in self.alfabeto:
                raise KeyError(f"Error léxico en token {indice}: {accion}")

        recorrido = []

        for accion in tokens:
            self.paso(accion, recorrido)
        if self.estado != "q_funcionando" or not self.pila.pila_vacia():
            raise ValueError(f"Rechazado por final invalido, {self.estado}, quedando en la pila {self.pila.mostrar_pila()}")

        return recorrido, self.pila.cantidad_pila