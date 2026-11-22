# Robot Recolector — Grupo 8 (Arquitectura MVC con Flask)

## Estructura del Proyecto (MVC)
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
- `app.py`: Servidor web **Flask** que conecta las rutas HTTP con el controlador y la vista.

## Como ejecutar
1. Instalar Flask (si no está instalado):
   
  ""pip install flask""
  
2. Ejecutar la aplicación desde la carpeta `Trabajo_Promocion_FTI_Robot_Grupo8`:
   
   "python app.py"
   
3. Abrir el navegador en `http://127.0.0.1:5000`.
