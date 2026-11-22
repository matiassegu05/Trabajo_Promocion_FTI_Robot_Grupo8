import csv
import io
from modelo.automataPila import AutomataPila
from modelo.robot import Robot
from modelo.tablero import Tablero


def crear_instancia_g08():
    tablero = Tablero(
        filas=6,
        columnas=6,
        obstaculos=[(2, 2), (2, 4), (3, 4), (5, 3)],
        cajas=[(1, 1), (1, 5), (2, 3), (3, 6)],
        destinos=[(3, 1), (4, 1), (5, 1), (6, 1)],
    )
    robot = Robot(posicion_inicial=(6, 2))
    return tablero, robot


def snapshot_estado(tablero, robot, indice=0, orden="INICIO", estado_ap="q0", pila="Z0"):
    return {
        "indice": indice,
        "orden": orden,
        "estado_ap": estado_ap,
        "pila": pila,
        "posicion": list(robot.posicion_actual),
        "con_carga": robot.con_carga,
        "cajas": [list(c) for c in sorted(tablero.cajas)],
    }


def ejecutar_programa_mvc(cadena: str):
    automata = AutomataPila()
    tablero, robot = crear_instancia_g08()

    config_grilla = {
        "filas": tablero.filas,
        "columnas": tablero.columnas,
        "obstaculos": [list(o) for o in sorted(tablero.obstaculos)],
        "destinos": [list(d) for d in sorted(tablero.destinos)],
        "robot_inicial": list(robot.posicion_inicial),
    }

    pasos_visuales = [snapshot_estado(tablero, robot)]

    #validación léxica y sintáctica (Autómata de Pila)
    try:
        recorrido, altura_max = automata.validar(cadena)
    except KeyError as error:
        return {
            "categoria": "ERROR LÉXICO",
            "exito": False,
            "mensaje": error.args[0],
            "config": config_grilla,
            "pasos": pasos_visuales,
            "metricas": {"sin_carga": 0, "con_carga": 0, "max_pila": 0, "total_tokens": len(cadena.split())},
            "csv": "",
        }
    except ValueError as error:
        return {
            "categoria": "RECHAZO DEL AP",
            "exito": False,
            "mensaje": str(error),
            "config": config_grilla,
            "pasos": pasos_visuales,
            "metricas": {"sin_carga": 0, "con_carga": 0, "max_pila": 0, "total_tokens": len(cadena.split())},
            "csv": "",
        }

    #Simulación fisica paso a paso
    sin_carga = 0
    con_carga = 0
    filas_csv = []

    for indice, accion, estado, pila in recorrido:
        try:
            robot.ejecutar_accion(accion, tablero)
        except ValueError as error:
            return {
                "categoria": "ERROR FÍSICO",
                "exito": False,
                "mensaje": f"Error en token {indice} ('{accion}'): {error}",
                "config": config_grilla,
                "pasos": pasos_visuales,
                "metricas": {
                    "sin_carga": sin_carga,
                    "con_carga": con_carga,
                    "max_pila": altura_max,
                    "total_tokens": len(recorrido),
                },
                "csv": generar_csv_texto(filas_csv),
            }

        if accion in robot.Movimientos:
            if robot.con_carga:
                con_carga += 1
            else:
                sin_carga += 1

        carga_txt = "Si" if robot.con_carga else "No"
        filas_csv.append([indice, accion, estado, pila, str(robot.posicion_actual), carga_txt])
        pasos_visuales.append(snapshot_estado(tablero, robot, indice, accion, estado, pila))

    #Para la verificación de la meta final
    meta_cumplida = (
        tablero.comprobar_cajas()
        and robot.posicion_actual == robot.posicion_inicial
        and not robot.con_carga
    )

    categoria = "MISIÓN RESUELTA" if meta_cumplida else "OBJETIVO NO ALCANZADO"
    mensaje = (
        "Todas las cajas llegaron a destino y el robot regresó a (6, 2) con pinza vacía."
        if meta_cumplida
        else f"Programa válido, pero la meta no se completó. Posición final: {robot.posicion_actual}."
    )

    return {
        "categoria": categoria,
        "exito": meta_cumplida,
        "mensaje": mensaje,
        "config": config_grilla,
        "pasos": pasos_visuales,
        "metricas": {
            "sin_carga": sin_carga,
            "con_carga": con_carga,
            "max_pila": altura_max,
            "total_tokens": len(recorrido),
        },
        "csv": generar_csv_texto(filas_csv),
    }


def generar_csv_texto(filas):
    salida = io.StringIO()
    writer = csv.writer(salida)
    writer.writerow(["indice", "orden", "estado_pila", "pila", "posicion", "carga"])
    writer.writerows(filas)
    return salida.getvalue()
