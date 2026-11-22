from flask import Flask, render_template, request, jsonify
from controlador.simulador_controller import ejecutar_programa_mvc, crear_instancia_g08, snapshot_estado

app = Flask(
    __name__,
    template_folder="vista/templates",
    static_folder="vista/static"
)


@app.route("/")
def index():
    tablero, robot = crear_instancia_g08()
    estado_inicial = {
        "config": {
            "filas": tablero.filas,
            "columnas": tablero.columnas,
            "obstaculos": [list(o) for o in sorted(tablero.obstaculos)],
            "destinos": [list(d) for d in sorted(tablero.destinos)],
            "robot_inicial": list(robot.posicion_inicial),
        },
        "paso_0": snapshot_estado(tablero, robot),
    }
    return render_template("index.html", estado_inicial=estado_inicial)


@app.route("/api/simular", methods=["POST"])
def simular():
    datos = request.get_json(silent=True) or {}
    cadena = datos.get("programa", "")
    resultado = ejecutar_programa_mvc(cadena)
    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
