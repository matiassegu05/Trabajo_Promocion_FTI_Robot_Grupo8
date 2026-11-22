# Robot Recolector - Grupo 08

Implementación en Python de un analizador léxico, un autómata de pila (AP) y un simulador sobre grilla 6x6 para el Trabajo Práctico de Promoción de Fundamentos Teóricos de la Informática.

## Tablero

- Grilla: 6 filas x 6 columnas (coordenadas `(fila, columna)` desde `(1, 1)` arriba a la izquierda).
- Posición inicial y final del robot: `(6, 2)`.
- Cajas iniciales: `(1, 1)`, `(1, 5)`, `(2, 3)`, `(3, 6)`.
- Obstáculos: `(2, 2)`, `(2, 4)`, `(3, 4)`, `(5, 3)`.
- Destinos finales: `(3, 1)`, `(4, 1)`, `(5, 1)`, `(6, 1)`.

## Requisitos

- Python 3.10 o superior.

## Estructura del proyecto

- `main.py`: punto de entrada. instancia tablero, carga el archivo de prueba, invoca la validación del autómata, ejecuta la simulación y exporta el registro a CSV.
- `automataPila.py`: implementa la verificación léxica y el autómata de pila que controla el protocolo de viajes.
- `pila.py`: estructura de pila con marcador de fondo `Z0` y seguimiento de la altura máxima alcanzada.
- `robot.py`: modela la posición del robot, la pinza de carga y la ejecución de movimientos sobre el tablero.
- `tablero.py`: administra la grilla, obstáculos, cajas, destinos, validaciones físicas y visualización en consola.
- `prueba1.txt` a `prueba11.txt`: archivos de entrada con la solución completa de la instancia y los casos de prueba exigidos por la consigna.

## Funcionamiento general

El programa opera en dos etapas:

1. Validación léxica y sintáctica (`AutomataPila`):
   - Tokens válidos: `arriba`, `abajo`, `izquierda`, `derecha`, `agarrar`, `soltar`, `viaje`, `finviaje`.
   - Estados del AP: `q0`, `q_moviendose`, `q_volviendo`, `q_terminado` y `q_funcionando`.
   - En cada `viaje`, el AP apila el movimiento inverso (`ARR`, `AB`, `IZ`, `DR`) por cada desplazamiento de ida y exige desapilarlos en orden exacto tras `agarrar`, antes de permitir `soltar` y `finviaje`.
   - Se exige al menos un viaje completo; la entrada vacía es rechazada.

2. Simulación física (`Tablero` y `Robot`):
   - Solo se ejecuta si la cadena fue aceptada por el AP.
   - Controla límites de la grilla, obstáculos, disponibilidad de cajas al agarrar, celdas libres al soltar y cumplimiento de la meta final (todas las cajas en destino, robot en `(6, 2)` y pinza vacía).

## Cómo ejecutar

1. Abrir una terminal en la carpeta raíz del proyecto.
2. Ejecutar:

```bash
python main.py
