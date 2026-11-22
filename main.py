import csv
import time
from automataPila import AutomataPila
from robot import Robot
from tablero import Tablero

def crear_tablero():
    tablero = Tablero(
        filas=6,
        columnas=6,
        obstaculos=[(2, 2), (2, 4), (3, 4), (5, 3)],
        cajas=[(1, 1), (1, 5), (2, 3), (3, 6)],
        destinos=[(3, 1), (4, 1), (5, 1), (6, 1)],    
    )
    robot = Robot(posicion_inicial=(6, 2))
    return tablero, robot

def guardar_csv(filas, nombre):
    with open(f"{nombre}.csv", "w", newline="",encoding="utf-8") as archivo:
        texto = csv.writer(archivo)
        texto.writerow(["indice", "orden", "estado_pila", "pila", "posicion", "carga"])
        texto.writerows(filas)

def ejecutar_simulacion():
    automata = AutomataPila()
    tablero, robot = crear_tablero()

    print("Tablero:")
    tablero.mostrar(robot.posicion_actual, robot.con_carga)

    numero_txt = input("Ingrese el numero de la prueba que quiere realizar (ej: 1 para prueba1.txt): ")
    nombre = f"prueba{numero_txt}"
    with open(f"{nombre}.txt", "r", encoding="utf-8") as archivo:
        cadena = archivo.read()

    try:
        recorrido, altura_max = automata.validar(cadena)
    except KeyError as error:
        print(f"\nRESULTADO: ERROR LÉXICO:  {error.args[0]}")
        return
    except ValueError as error:
        print(f"\nRESULTADO: RECHAZO DEL AUTOMATA DE PLIA: {error}")
        return

    filas = []
    sin_carga = 0
    con_carga = 0

    for indice, accion, estado, pila in recorrido:
        try:
            robot.ejecutar_accion(accion, tablero)
        except ValueError as error:
            guardar_csv(filas, nombre)
            print(f"RESULTADO: ERROR en paso {indice} ('{accion}') -> {error}")
            return

        if accion in robot.Movimientos:
            if robot.con_carga:
                con_carga += 1
            else:
                sin_carga += 1

        carga = "Si" if robot.con_carga else "No"
        filas.append([indice, accion, estado, pila, robot.posicion_actual, carga])
    guardar_csv(filas, nombre)
    print("\nCadena válida y guardado en {nombre}.csv. Iniciando simulación...\n")
    tablero_terminal, robot_terminal = crear_tablero()
    for indice, accion, estado, pila in recorrido:
        robot_terminal.ejecutar_accion(accion, tablero_terminal)
        carga = "Sí" if robot_terminal.con_carga else "No"
        print(f"Paso {indice}: {accion} | Estado: {estado} | Pos: {robot_terminal.posicion_actual} | Carga: {carga} | Pila: {pila}")
        tablero_terminal.mostrar(robot_terminal.posicion_actual, robot_terminal.con_carga)
        time.sleep(1)
    print(f"Movimientos sin carga: {sin_carga}")
    print(f"Movimientos con carga: {con_carga}")
    print(f"Altura máxima de pila (sin Z0): {altura_max}")
    if (tablero.comprobar_cajas() and robot.posicion_actual == robot.posicion_inicial and not robot.con_carga):
        print("RESULTADO: MISIÓN RESUELTA")
    else:
        print("RESULTADO: OBJETIVO NO ALCANZADO")


if __name__ == "__main__":
    ejecutar_simulacion()