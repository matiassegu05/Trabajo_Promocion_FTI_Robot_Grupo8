# Robot Recolector - Grupo 8 (Arquitectura MVC con Flask)

Implementación en Python de un analizador léxico, un autómata de pila (AP) y un simulador sobre grilla 6x6.

## Tablero

- Grilla: 6 filas x 6 columnas (coordenadas `(fila, columna)` desde `(1, 1)` arriba a la izquierda).
- Posición inicial y final del robot: `(6, 2)`.
- Cajas iniciales: `(1, 1)`, `(1, 5)`, `(2, 3)`, `(3, 6)`.
- Obstáculos: `(2, 2)`, `(2, 4)`, `(3, 4)`, `(5, 3)`.
- Destinos finales: `(3, 1)`, `(4, 1)`, `(5, 1)`, `(6, 1)`.

## Requisitos

- Python 3.10 o superior.

## Estructura del proyecto

- `modelo/`: Lógica pura del dominio sin interfaz (clases originales adaptadas):
  - `pila.py`: Estructura LIFO con marcador `Z0`.
  - `automataPila.py`: Autómata de Pila Determinista (`ARR`, `AB`, `IZ`, `DR`).
  - `robot.py`: Estado de posición, carga y validación de acciones.
  - `tablero.py`: Grilla 6x6, obstáculos, cajas y destinos del Grupo 08.
- `controlador/`:
  - `simulador_controller.py`: Orquesta la validación con `AutomataPila`, ejecuta paso a paso en `Robot` y `Tablero`, calcula métricas y arma la respuesta JSON/CSV.
- `vista/`:
  - `templates/index.html`: Plantilla HTML renderizada por Flask.
  - `static/css/estilos.css`: Estilos de la interfaz, grilla 6x6 y pila visual.
  - `static/js/app.js`: Control de animación paso a paso, carga de pruebas y descarga de CSV.
  - `static/img/wall-e.jpg`: Imagen del robot.
- `app.py`: Servidor web **Flask** que conecta las rutas HTTP con el controlador y la vista.

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

1. Instalar Flask (si no está instalado):
   
  ""pip install flask""
  
2. Ejecutar la aplicación desde la carpeta `Trabajo_Promocion_FTI_Robot_Grupo8`:
   
  "python app.py"
   
3. Abrir el navegador en `http://127.0.0.1:5000`.

4. En Programa de Órdenes - Cargar caso de prueba, seleccionar solucion completa grupo 8 (68 tokens) o cualquier caso
de prueba que quiera visualizar.

5. Tocar Validar y simular para ejecutar la resolucion.

6. Presionar Descargar CSV para obtener el registro de la solución (en caso de aparecer deshabilitado el boton es debido a que ocurre un rechazo en el AP o un Error Fisico).