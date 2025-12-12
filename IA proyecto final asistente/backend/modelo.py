from diagnosticos import diagnostico_boot, soluciones_boot
import json

estado_usuario = {
    "modo": None,
    "paso": None
}

def responder(pregunta):

    pregunta = pregunta.lower()

    # --- INICIAR DIAGNÓSTICO AVANZADO DE LINUX NO ARRANCA ---
    intenciones_boot = [
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
        "linux no bootea"
    ]

    # Detección avanzada de intención por frase exacta o similar
    for frase in intenciones_boot:
        if frase in pregunta:
            estado_usuario["modo"] = "diagnostico_boot"
            estado_usuario["paso"] = 1
            return diagnostico_boot[1]["pregunta"]

    # Coincidencia flexible por palabras clave
    if ("linux" in pregunta and "arranca" in pregunta) or \
       ("ubuntu" in pregunta and "arranca" in pregunta):

        estado_usuario["modo"] = "diagnostico_boot"
        estado_usuario["paso"] = 1
        return diagnostico_boot[1]["pregunta"]

    # --- SI YA ESTÁ EN DIAGNÓSTICO ---
    if estado_usuario["modo"] == "diagnostico_boot":
        paso = estado_usuario["paso"]
        nodo = diagnostico_boot[paso]

        if pregunta == "sí" or pregunta == "si":
            siguiente = nodo["si"]
            if type(siguiente) == int:
                estado_usuario["paso"] = siguiente
                return diagnostico_boot[siguiente]["pregunta"]
            else:
                estado_usuario["modo"] = None
                return soluciones_boot[siguiente]

        elif pregunta == "no":
            resultado = nodo["no"]
            estado_usuario["modo"] = None
            return soluciones_boot[resultado]

        else:
            return "Responde con 'sí' o 'no', por favor."

    # --- RESPUESTAS NORMALES (base de conocimiento) ---
    with open("base_conocimiento.json") as f:
        data = json.load(f)

    for item in data:
        for kw in item["keywords"]:
            if kw in pregunta:
                return item["respuesta"]

    return "No entiendo completamente. ¿Deseas iniciar un diagnóstico?"
