import time
from automataPila import AutomataPila
from robot import Robot
from tablero import Tablero


def ejecutar_simulacion():
    tablero = Tablero(
        filas=6,
        columnas=6,
        obstaculos=[(2, 2), (2, 4), (3, 4), (5, 3)],
        cajas=[(1, 1), (1, 5), (2, 3), (3, 6)],
        destinos=[(3, 1), (4, 1), (5, 1), (6, 1)],
    )
    robot = Robot(posicion_inicial=(6, 2))
    automata = AutomataPila()

    print("Tablero:")
    tablero.mostrar(robot.posicion_actual, robot.con_carga)

    cadena = input("Ingresá la cadena completa de órdenes:")

    try:
        recorrido, altura_max = automata.validar(cadena)
    except KeyError as error:
        print(f"\nRESULTADO: ERROR LÉXICO:  {error.args[0]}")
        return
    except ValueError as error:
        print(f"\nRESULTADO: RECHAZO DEL AUTOMATA DE PLIA: {error}")
        return

    print("\nCadena válida. Iniciando simulación...\n")

    for indice, accion, estado, pila in recorrido:
        try:
            robot.ejecutar_accion(accion, tablero)
        except ValueError as error:
            print(f"RESULTADO: ERROR FÍSICO en paso {indice} ('{accion}') -> {error}")
            return

        carga = "Sí" if robot.con_carga else "No"
        print(f"Paso {indice}: {accion} | Estado: {estado} | Pos: {robot.posicion_actual} | Carga: {carga} | Pila: {pila}")
        tablero.mostrar(robot.posicion_actual, robot.con_carga)
        time.sleep(1)

    print(f"Altura máxima de pila (sin Z0): {altura_max}")
    if (tablero.comprobar_cajas() and robot.posicion_actual == robot.posicion_inicial and not robot.con_carga):
        print("RESULTADO: MISIÓN RESUELTA")
    else:
        print("RESULTADO: OBJETIVO NO ALCANZADO")


if __name__ == "__main__":
    ejecutar_simulacion()