# LINUBOT – Asistente tipo terminal

Proyecto frontend de una interfaz de chat estilo terminal con efecto “Matrix”, que se conecta a un backend vía HTTP para obtener respuestas.

## Estructura del proyecto

```
IA proyecto final asistente/
├─ index.html        # Página principal (usa CSS y JS externos)
├─ style.css         # Estilos de la UI tipo terminal
└─ script.js         # Lógica de efecto matrix y chat (fetch al backend)
```

## Requisitos

- Navegador moderno (Chrome, Edge, Firefox, Safari).
- Backend HTTP disponible en `http://192.168.0.109:5001/chat` que acepte POST con JSON `{ "pregunta": string }` y devuelva JSON `{ "respuesta": string }`.
- Si el frontend y backend están en orígenes distintos, se requiere que el backend permita CORS para el origen del frontend.

## Ejecución

1. Backend
   - Asegúrate de tener un servidor corriendo en `http://192.168.0.109:5001` con un endpoint POST `/chat` que responda con el formato esperado.
   - Ejemplo de contrato:
     - Request: `POST /chat` con body `{"pregunta":"¿Qué es Linux?"}`
     - Response: `{"respuesta":"Linux es un sistema operativo..."}`

2. Frontend
   - Opción A (recomendada): servir archivos estáticos con un servidor local.
     - Por ejemplo, con Node.js instalado: `npx serve "IA proyecto final asistente"` y abrir la URL que se indique.
   - Opción B: abrir directamente `index.html` en el navegador (doble clic). Nota: si el backend está en otro origen, CORS podría bloquear la petición.
   - Alternativa: abrir `asistente.html` (versión auto-contenida) en el navegador.

## Uso

- Al cargar, verás la interfaz tipo terminal con el efecto Matrix.
- Escribe tu consulta en el campo de entrada y presiona Enter o el botón Enviar.
- El sistema mostrará tu mensaje, un indicador de “escribiendo”, y finalmente la respuesta del backend.

## Configuración del endpoint

Actualmente, la URL del backend está codificada en `script.js` y `asistente.html`:
```
fetch("http://192.168.0.109:5001/chat", { ... })
```
Sugerencias para parametrizar:
- Usar una variable global definida en `index.html` (ej. `window.API_BASE`), y leerla desde `script.js`.
- Leer desde `localStorage` o desde una meta/atributo `data-*` del HTML.
- Usar ruta relativa (`/chat`) si sirves frontend y backend desde el mismo host/puerto.

## Manejo de errores

- Si hay problemas de red/CORS o el backend no responde, se mostrará: `[ERROR] Conexión perdida. Reintentando...`.
- Recomendaciones:
  - Diferenciar errores de red vs. HTTP no-200.
  - Implementar reintentos con backoff y un mensaje más detallado.

## Personalización

- Estilos: editar `style.css` para cambiar colores, tipografías o animaciones.
- Efecto Matrix: ajustar `fontSize`, intervalo (`setInterval(drawMatrix, 50)`), o el set de caracteres en `script.js`.
- UI inicial: el mensaje de bienvenida está en `index.html` (y en `asistente.html`), dentro del primer bloque `.bot-msg`.

## Notas sobre las dos variantes

- `index.html` + `style.css` + `script.js`: más mantenible al separar responsabilidades.
- `asistente.html`: práctico para compartir un único archivo; puede divergir si se hacen cambios en los archivos externos. Mantener una sola fuente de la verdad o documentar el flujo de actualizaciones.

## Compatibilidad y rendimiento

- Probado con viewport responsive; el canvas se adapta al tamaño de la ventana.
- En dispositivos de bajos recursos, aumentar el intervalo del render (por ej. 70–100 ms) puede mejorar el rendimiento.

## Licencia

Define aquí la licencia del proyecto (MIT, Apache-2.0, etc.) si corresponde.
