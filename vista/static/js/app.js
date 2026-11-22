const PRESETS = {
  solucion: `izquierda arriba arriba arriba 
viaje arriba arriba agarrar abajo abajo soltar finviaje 
abajo 
viaje derecha arriba derecha arriba agarrar abajo izquierda abajo izquierda soltar finviaje 
abajo 
viaje derecha arriba derecha derecha derecha arriba arriba arriba agarrar abajo abajo abajo izquierda izquierda izquierda abajo izquierda soltar finviaje 
abajo 
viaje derecha derecha derecha derecha derecha arriba arriba arriba agarrar abajo abajo abajo izquierda izquierda izquierda izquierda izquierda soltar finviaje 
derecha
`,
  regreso_mal: "izquierda arriba arriba arriba viaje arriba arriba agarrar abajo izquierda soltar finviaje",
  soltar_antes: "izquierda arriba arriba arriba viaje arriba arriba agarrar abajo soltar abajo finviaje",
  sin_finviaje: "izquierda arriba arriba arriba viaje arriba arriba agarrar abajo abajo soltar",
  doble_agarrar: "izquierda arriba arriba arriba viaje arriba arriba agarrar agarrar abajo abajo soltar finviaje",
  obstaculo: "viaje arriba arriba arriba arriba derecha agarrar izquierda abajo abajo abajo abajo soltar finviaje",
  agarrar_vacio: "viaje arriba agarrar abajo soltar finviaje",
  sin_meta: "arriba arriba arriba izquierda viaje arriba arriba agarrar abajo abajo soltar finviaje",
  lexico: "izquierda diagonal viaje arriba agarrar abajo soltar finviaje",
  vacia: "",
  fuera_grilla: "abajo viaje arriba agarrar abajo soltar finviaje"
};

let configGrilla = window.ESTADO_INICIAL.config;
let pasos = [window.ESTADO_INICIAL.paso_0];
let indiceActual = 0;
let timerPlay = null;
let ultimoCsv = "";

const txtPrograma = document.getElementById("txtPrograma");
const selectPreset = document.getElementById("selectPreset");
const btnValidar = document.getElementById("btnValidar");
const btnDescargarCsv = document.getElementById("btnDescargarCsv");
const bannerResultado = document.getElementById("bannerResultado");
const contenedorGrilla = document.getElementById("contenedorGrilla");
const visualPila = document.getElementById("visualPila");
const tbodyTraza = document.querySelector("#tablaTraza tbody");

txtPrograma.value = PRESETS.solucion;

selectPreset.addEventListener("change", () => {
  txtPrograma.value = PRESETS[selectPreset.value] ?? "";
});

function mismaPos(a, b) {
  return a[0] === b[0] && a[1] === b[1];
}

function existeEnLista(lista, pos) {
  return lista.some((item) => mismaPos(item, pos));
}

function renderizarPaso(idx) {
  detenerReproduccion();
  mostrarPaso(idx);
}

function mostrarPaso(idx) {
  if (idx < 0 || idx >= pasos.length) return;
  indiceActual = idx;
  const paso = pasos[idx];

  document.getElementById("lblPasoActual").textContent = `Paso ${idx} / ${pasos.length - 1}`;
  document.getElementById("lblEstadoAp").textContent = paso.estado_ap;
  document.getElementById("lblTokenActual").textContent = paso.orden;
  document.getElementById("lblPosCarga").textContent = `(${paso.posicion[0]}, ${paso.posicion[1]}) · ${paso.con_carga ? "Con caja" : "Vacía"}`;

  // para renderizar pila (tope arriba)
  visualPila.innerHTML = "";
  const simbolos = paso.pila.split(" ");
  simbolos.forEach((simb) => {
    const div = document.createElement("div");
    div.className = "pila-item" + (simb === "Z0" ? " pila-z0" : "");
    div.textContent = simb === "Z0" ? "Z0 (fondo)" : simb;
    visualPila.appendChild(div);
  });

  // para renderizar la grilla 6x6 con coordenadas
  contenedorGrilla.innerHTML = "";
  const esquina = document.createElement("div");
  esquina.className = "celda-coord";
  contenedorGrilla.appendChild(esquina);

  for (let c = 1; c <= configGrilla.columnas; c++) {
    const colHdr = document.createElement("div");
    colHdr.className = "celda-coord";
    colHdr.textContent = c;
    contenedorGrilla.appendChild(colHdr);
  }

  for (let f = 1; f <= configGrilla.filas; f++) {
    const rowHdr = document.createElement("div");
    rowHdr.className = "celda-coord";
    rowHdr.textContent = f;
    contenedorGrilla.appendChild(rowHdr);

    for (let c = 1; c <= configGrilla.columnas; c++) {
      const pos = [f, c];
      const celda = document.createElement("div");
      celda.className = "celda";

      const esRobot = mismaPos(paso.posicion, pos);
      const esObstaculo = existeEnLista(configGrilla.obstaculos, pos);
      const esCaja = existeEnLista(paso.cajas, pos);
      const esDestino = existeEnLista(configGrilla.destinos, pos);

      let contenidoVisual = "";
      if (esDestino) celda.classList.add("destino");
      if (esObstaculo) {
        celda.classList.add("obstaculo");
        contenidoVisual = `<span>X</span>`;
      } else if (esRobot) {
        celda.classList.add(paso.con_carga ? "robot-carga" : "robot");
        const walleSrc = window.WALLE_IMG_URL || "/static/img/walle.png";
        const badgeCarga = paso.con_carga ? `<span style="font-size:0.55rem;color:#fef08a;">★ CARGA</span>` : "";
        contenidoVisual = `<img src="${walleSrc}" alt="WALL-E" class="walle-avatar" />${badgeCarga}`;
      } else if (esCaja) {
        celda.classList.add("caja");
        contenidoVisual = `<span>C</span>`;
      } else if (esDestino) {
        contenidoVisual = `<span>T</span>`;
      }

      celda.innerHTML = `${contenidoVisual}<small>(${f},${c})</small>`;
      contenedorGrilla.appendChild(celda);
    }
  }

  
  document.querySelectorAll("#tablaTraza tbody tr").forEach((tr) => {
    tr.classList.toggle("activa", Number(tr.dataset.paso) === idx);
  });
}

function poblarTablaTraza() {
  tbodyTraza.innerHTML = "";
  for (let i = 1; i < pasos.length; i++) {
    const p = pasos[i];
    const tr = document.createElement("tr");
    tr.dataset.paso = i;
    tr.innerHTML = `
      <td>${p.indice}</td>
      <td>${p.orden}</td>
      <td>${p.estado_ap}</td>
      <td>${p.pila}</td>
      <td>(${p.posicion[0]},${p.posicion[1]})</td>
      <td>${p.con_carga ? "Sí" : "No"}</td>
    `;
    tr.addEventListener("click", () => renderizarPaso(i));
    tbodyTraza.appendChild(tr);
  }
}

async function ejecutarSimulacion() {
  detenerReproduccion();
  const resp = await fetch("/api/simular", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ programa: txtPrograma.value }),
  });
  const data = await resp.json();

  configGrilla = data.config;
  pasos = data.pasos;
  ultimoCsv = data.csv || "";
  btnDescargarCsv.disabled = !ultimoCsv;

  bannerResultado.className = "banner " + (data.exito ? "ok" : (data.categoria === "OBJETIVO NO ALCANZADO" ? "warn" : "error"));
  bannerResultado.innerHTML = `<strong>${data.categoria}:</strong> ${data.mensaje}`;

  document.getElementById("mSinCarga").textContent = data.metricas.sin_carga;
  document.getElementById("mConCarga").textContent = data.metricas.con_carga;
  document.getElementById("mMaxPila").textContent = data.metricas.max_pila;
  document.getElementById("mTokens").textContent = data.metricas.total_tokens;

  poblarTablaTraza();
  mostrarPaso(0);
  if (pasos.length > 1) iniciarReproduccion();
}

function iniciarReproduccion() {
  detenerReproduccion();
  const vel = Number(document.getElementById("selectVelocidad").value);
  document.getElementById("btnPlay").textContent = "⏸ Pausar";
  timerPlay = setInterval(() => {
    if (indiceActual < pasos.length - 1) {
      mostrarPaso(indiceActual + 1);
    } else {
      detenerReproduccion();
    }
  }, vel);
}

function detenerReproduccion() {
  if (timerPlay) {
    clearInterval(timerPlay);
    timerPlay = null;
  }
  document.getElementById("btnPlay").textContent = "▶ Reproducir";
}

btnValidar.addEventListener("click", ejecutarSimulacion);
document.getElementById("btnInicio").addEventListener("click", () => renderizarPaso(0));
document.getElementById("btnAnterior").addEventListener("click", () => renderizarPaso(indiceActual - 1));
document.getElementById("btnSiguiente").addEventListener("click", () => renderizarPaso(indiceActual + 1));
document.getElementById("btnFinal").addEventListener("click", () => renderizarPaso(pasos.length - 1));

document.getElementById("btnPlay").addEventListener("click", () => {
  if (timerPlay) {
    detenerReproduccion();
  } else {
    if (indiceActual >= pasos.length - 1) mostrarPaso(0);
    iniciarReproduccion();
  }
});

btnDescargarCsv.addEventListener("click", () => {
  if (!ultimoCsv) return;
  const blob = new Blob([ultimoCsv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "registro_ejecucion_g08.csv";
  a.click();
  URL.revokeObjectURL(url);
});

mostrarPaso(0);
