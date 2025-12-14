import os
import json
from diagnosticos import (
    diagnostico_boot,
    soluciones_boot,
    diagnostico_wifi,
    soluciones_wifi,
    diagnostico_audio,
    soluciones_audio,
    diagnostico_temp,
    soluciones_temp,
    diagnostico_espacio,
    soluciones_espacio,
    diagnostico_apt,
    soluciones_apt,
    diagnostico_bluetooth,
    soluciones_bluetooth,
    diagnostico_impresora,
    soluciones_impresora,
    diagnostico_lento,
    soluciones_lento,
    diagnostico_nginx,
    soluciones_nginx,
)

# Estado por sesión
# session_states: {
#   session_id: {"modo": str|None, "paso": int|None, "arbol": str|None}
# }
session_states = {}

# Carga de base de conocimiento una sola vez con ruta robusta
BASE_DIR = os.path.dirname(__file__)
BASE_CONOCIMIENTO_PATH = os.path.join(BASE_DIR, "base_conocimiento.json")
try:
    with open(BASE_CONOCIMIENTO_PATH, encoding="utf-8") as f:
        BASE_CONOCIMIENTO = json.load(f)
except Exception as e:
    # Si falla la carga, deja una base mínima para no romper el servicio
    BASE_CONOCIMIENTO = []


def _get_state(session_id: str):
    if not session_id:
        session_id = "default"
    return session_states.setdefault(session_id, {"modo": None, "paso": None, "arbol": None})


def _set_state(session_id: str, modo=None, paso=None, arbol=None):
    state = _get_state(session_id)
    if modo is not None:
        state["modo"] = modo
    if paso is not None:
        state["paso"] = paso
    if arbol is not None:
        state["arbol"] = arbol


def _reset_state(session_id: str):
    session_states[session_id] = {"modo": None, "paso": None, "arbol": None}


# Registro de árboles de diagnóstico disponibles
DIAGNOSTICOS = {
    "boot": (diagnostico_boot, soluciones_boot),
    "wifi": (diagnostico_wifi, soluciones_wifi),
    "audio": (diagnostico_audio, soluciones_audio),
    "temp": (diagnostico_temp, soluciones_temp),
    "espacio": (diagnostico_espacio, soluciones_espacio),
    "apt": (diagnostico_apt, soluciones_apt),
    "bluetooth": (diagnostico_bluetooth, soluciones_bluetooth),
    "impresora": (diagnostico_impresora, soluciones_impresora),
    "lento": (diagnostico_lento, soluciones_lento),
    "nginx": (diagnostico_nginx, soluciones_nginx),
}


# Frases de intención para el diagnóstico de arranque (boot)
INTENCIONES_BOOT = [
    "linux no arranca",
    "no arranca linux",
    "mi pc con linux no arranca",
    "ubuntu no arranca",
    "mi linux no inicia",
    "problemas al arrancar linux",
    "pantalla negra linux",
    "no inicia ubuntu",
    "no puedo iniciar linux",
    "linux no enciende",
    "linux se queda en pantalla negra",
    "linux no bootea",
]

# Frases de intención para WiFi
INTENCIONES_WIFI = [
    "no conecta wifi",
    "no se conecta wifi",
    "no tengo wifi",
    "sin wifi",
    "problemas de wifi",
    "problemas con wifi",
    "wifi desconectado",
    "no aparece wifi",
    "no veo redes wifi",
    "wifi no funciona",
]

# Frases de intención para Audio
INTENCIONES_AUDIO = [
    "sin audio",
    "no hay audio",
    "no se oye",
    "no suena",
    "problemas de audio",
    "no se escucha",
    "audio no funciona",
]

# Frases de intención para Temperatura
INTENCIONES_TEMP = [
    "caliente",
    "sobrecalentamiento",
    "temperatura alta",
    "ventilador alto",
    "throttling",
]

# Frases de intención para Espacio en disco
INTENCIONES_ESPACIO = [
    "disco lleno",
    "sin espacio",
    "no space left on device",
    "particion llena",
]

# Frases de intención para APT roto
INTENCIONES_APT = [
    "apt roto",
    "dpkg interrupted",
    "dependencias rotas",
    "no puedo instalar paquetes",
]

# Frases de intención para Bluetooth
INTENCIONES_BLUETOOTH = [
    "bluetooth no conecta",
    "no conecta bluetooth",
    "bluetooth no funciona",
    "problemas bluetooth",
]

# Frases de intención para Impresora
INTENCIONES_IMPRESORA = [
    "impresora no imprime",
    "no imprime",
    "problemas impresora",
    "cola de impresion",
]

# Frases de intención para Lento/Rendimiento
INTENCIONES_LENTO = [
    "lento",
    "va lento",
    "rendimiento",
    "se traba",
]

# Frases de intención para Nginx
INTENCIONES_NGINX = [
    "nginx no arranca",
    "nginx caido",
    "nginx 502",
    "nginx 504",
    "nginx error",
]


def _normaliza(texto: str) -> str:
    return (texto or "").strip().lower()


def _es_respuesta_si(texto: str) -> bool:
    t = _normaliza(texto)
    return t in {"si", "sí", "s", "y", "yes"}


def _es_respuesta_no(texto: str) -> bool:
    t = _normaliza(texto)
    return t in {"no", "n"}


def _activar_arbol(session_id: str, nombre_arbol: str) -> str:
    _set_state(session_id, modo="diagnostico", paso=1, arbol=nombre_arbol)
    diagnostico, _ = DIAGNOSTICOS[nombre_arbol]
    return diagnostico[1]["pregunta"]


def responder(pregunta: str, session_id: str | None = None) -> str:
    """
    Orquestador de respuestas del asistente.
    - pregunta: texto del usuario
    - session_id: identificador de sesión (opcional). Si no se provee, usa "default".
    """
    pregunta = _normaliza(pregunta)
    session_id = session_id or "default"
    state = _get_state(session_id)

    # 1) Detección de intenciones para activar árboles
    if any(frase in pregunta for frase in INTENCIONES_BOOT) or (
        ("linux" in pregunta and "arranca" in pregunta) or ("ubuntu" in pregunta and "arranca" in pregunta)
    ):
        return _activar_arbol(session_id, "boot")

    if any(frase in pregunta for frase in INTENCIONES_WIFI):
        return _activar_arbol(session_id, "wifi")

    if any(frase in pregunta for frase in INTENCIONES_AUDIO):
        return _activar_arbol(session_id, "audio")

    if any(frase in pregunta for frase in INTENCIONES_TEMP):
        return _activar_arbol(session_id, "temp")

    if any(frase in pregunta for frase in INTENCIONES_ESPACIO):
        return _activar_arbol(session_id, "espacio")

    if any(frase in pregunta for frase in INTENCIONES_APT):
        return _activar_arbol(session_id, "apt")

    if any(frase in pregunta for frase in INTENCIONES_BLUETOOTH):
        return _activar_arbol(session_id, "bluetooth")

    if any(frase in pregunta for frase in INTENCIONES_IMPRESORA):
        return _activar_arbol(session_id, "impresora")

    if any(frase in pregunta for frase in INTENCIONES_LENTO):
        return _activar_arbol(session_id, "lento")

    if any(frase in pregunta for frase in INTENCIONES_NGINX):
        return _activar_arbol(session_id, "nginx")

    # 2) Si ya está en modo diagnóstico, navegar el árbol correspondiente (sí/no)
    if state["modo"] == "diagnostico" and state["arbol"] in DIAGNOSTICOS:
        diagnostico, soluciones = DIAGNOSTICOS[state["arbol"]]
        paso = state["paso"]
        nodo = diagnostico.get(paso)

        if not nodo:
            _reset_state(session_id)
            return "Ha ocurrido un error en el diagnóstico. Empecemos de nuevo."

        if _es_respuesta_si(pregunta):
            siguiente = nodo["si"]
            if isinstance(siguiente, int):
                _set_state(session_id, paso=siguiente)
                return diagnostico[siguiente]["pregunta"]
            else:
                # solución final
                _reset_state(session_id)
                return soluciones.get(siguiente, "No se encontró solución para este caso.")

        elif _es_respuesta_no(pregunta):
            resultado = nodo["no"]
            _reset_state(session_id)
            return soluciones.get(resultado, "No se encontró solución para este caso.")

        else:
            return "Responde con 'sí' o 'no', por favor."

    # 3) Búsqueda en base de conocimiento (keywords)
    for item in BASE_CONOCIMIENTO:
        try:
            keywords = item.get("keywords", [])
            respuesta = item.get("respuesta", "")
        except AttributeError:
            continue

        for kw in keywords:
            if kw.lower() in pregunta:
                return respuesta

    # 4) Mensaje por defecto
    return (
        "No entiendo completamente. Puedes decir: 'linux no arranca', 'no conecta wifi', 'sin audio', 'caliente', 'disco lleno', 'apt roto', 'bluetooth no conecta', 'impresora no imprime', 'va lento' o 'nginx 502' para iniciar un diagnóstico,"
        " o responde 'sí' para comenzar el de arranque."
    )