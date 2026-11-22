from pila import Pila

class AutomataPila:
    alfabeto ={"arriba", "abajo", "izquierda", "derecha", "agarrar", "soltar", "viaje", "finviaje"}

    inverso ={
        "arriba": "abajo",
        "abajo": "arriba",
        "izquierda": "derecha",
        "derecha": "izquierda",
    }

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
                self.pila.agregar(self.inverso[m])
            case ("q_moviendose", "agarrar"):
                self.estado = "q_volviendo"
            case ("q_volviendo",m) if m in self.inverso and tope == m:
                self.pila.sacar()
            case ("q_volviendo", "soltar") if tope == "Z0":
                self.estado = "q_terminado"
            case ("q_terminado", "finviaje") if tope == "Z0":
                self.estado = "q_funcionando"
            case _:
                raise ValueError(f"Se rechaza {accion}, queda en estado= {self.estado} y tope={tope}")

    def validar(self, cadena):
        self.reiniciar()
        tokens = cadena.split()

        if not tokens:
            raise ValueError("Error: la cadena esta vacia")
        
        for indice, accion in enumerate(tokens, start=1):
            if accion not in self.alfabeto:
                raise KeyError(f"Error léxico en token {indice}: {accion}")

        recorrido = []
        for indice, accion in enumerate(tokens, start=1):
            self.transicion(accion)
            recorrido.append((indice, accion, self.estado, self.pila.mostrar_pila()))

        if self.estado != "q_funcionando" or not self.pila.pila_vacia():
            raise ValueError(f"Rechazado por final invalido, {self.estado}, quedando en la pila {self.pila.mostrar_pila()}")
        
        return recorrido, self.pila.cantidad_pila

if __name__ == "__main__":
    ap = AutomataPila()
    programa = "derecha viaje arriba izquierda agarrar derecha abajo soltar finviaje"

    traza, altura_max = ap.validar(programa)
    for paso in traza:
        print(paso)
    print("Altura máxima:", altura_max)  