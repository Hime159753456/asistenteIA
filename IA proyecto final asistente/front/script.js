// Matrix effect
const canvas = document.getElementById('matrix');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
const fontSize = 14;
const columns = canvas.width / fontSize;
const drops = Array(Math.floor(columns)).fill(1);

function drawMatrix() {
    ctx.fillStyle = 'rgba(10, 14, 39, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#00ff41';
    ctx.font = fontSize + 'px monospace';

    for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        }
        drops[i]++;
    }
}

setInterval(drawMatrix, 50);

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

// Chat functionality
const chat = document.getElementById("chat");

function agregarMensaje(texto, tipo) {
    const fila = document.createElement("div");
    fila.classList.add("message-row");
    if (tipo === "user") fila.classList.add("user");

    const burbuja = document.createElement("div");
    burbuja.classList.add("message", tipo + "-msg");
    burbuja.innerText = texto;

    const avatar = document.createElement("div");
    avatar.classList.add("avatar");
    avatar.textContent = tipo === "user" ? "▶" : "⚡";

    if (tipo === "user") {
        fila.appendChild(burbuja);
        fila.appendChild(avatar);
    } else {
        fila.appendChild(avatar);
        fila.appendChild(burbuja);
    }

    chat.appendChild(fila);
    chat.scrollTop = chat.scrollHeight;
}

function mostrarEscribiendo() {
    const filaTyping = document.createElement("div");
    filaTyping.id = "typing";
    filaTyping.classList.add("message-row");

    const avatar = document.createElement("div");
    avatar.classList.add("avatar");
    avatar.textContent = "⚡";

    const typing = document.createElement("div");
    typing.classList.add("typing");
    typing.innerHTML = `
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    filaTyping.appendChild(avatar);
    filaTyping.appendChild(typing);
    chat.appendChild(filaTyping);
    chat.scrollTop = chat.scrollHeight;
}

function ocultarEscribiendo() {
    const escribir = document.getElementById("typing");
    if (escribir) escribir.remove();
}

async function enviar() {
    const input = document.getElementById("pregunta");
    const texto = input.value.trim();
    if (!texto) return;

    agregarMensaje(texto, "user");
    input.value = "";

    mostrarEscribiendo();
    //Se hace el llamado a la API
    try {
        const res = await fetch("https://overspeculative-kaycee-directorially.ngrok-free.dev/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pregunta: texto })
        });
    // Obtener la respuesta en formato JSON
        const data = await res.json();
        ocultarEscribiendo();
        agregarMensaje(data.respuesta, "bot");
    } catch (error) {
        ocultarEscribiendo();
        agregarMensaje("[ERROR] Conexión perdida. Reintentando...", "bot");
    }
}
