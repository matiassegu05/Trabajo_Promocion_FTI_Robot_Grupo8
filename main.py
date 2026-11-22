from robot import Robot
from tablero import Tablero


def mostrar_estado(robot, tablero):
    print(f"Posición: {robot.posicion_actual} | Carga: {'Sí' if robot.con_carga else 'No'}\n")
    tablero.mostrar(robot.posicion_actual, robot.con_carga)


def iniciar_simulacion():
    tablero = Tablero(
        filas=6,
        columnas=6,
        obstaculos=[(2, 2), (2, 4), (3, 4), (5, 3)],
        cajas=[(1, 1), (1, 5), (2, 3), (3, 6)],
        destinos=[(3,1), (4,1), (5,1), (6,1)],
    )
    robot = Robot(posicion_inicial=(6, 2))

    print("Comandos: arriba, abajo, izquierda, derecha, agarrar, soltar, viaje, finviaje")
    print("Escribí 'salir' para terminar.\n")
    mostrar_estado(robot, tablero)

    while True:
        orden = input("Orden > ").strip().lower()

        if orden == "salir":
            break
        if not orden:
            continue

        try:
            robot.ejecutar_accion(orden, tablero)
        except ValueError as error:
            print(f"Error: {error}\n")
            continue

        mostrar_estado(robot, tablero)

        if (
            tablero.comprobar_cajas()
            and robot.posicion_actual == robot.posicion_inicial
            and not robot.con_carga
        ):
            print("Misión cumplida: todas las cajas están en destino y el robot volvió al inicio.")
            break


if __name__ == "__main__":
    iniciar_simulacion()