# diagnosticos.py
# Motores expertos de diagnóstico

# --- Diagnóstico: Linux no arranca (boot) ---
diagnostico_boot = {
    1: {"pregunta": "¿Ves el menú de GRUB al encender la computadora? (sí/no)", "si": 2, "no": "sol_grub"},
    2: {"pregunta": "Después de seleccionar tu sistema, ¿ves texto cargando antes de que falle? (sí/no)", "si": 3, "no": "sol_kernel"},
    3: {"pregunta": "¿La pantalla se queda completamente negra después de cargar el kernel? (sí/no)", "si": "sol_grafico", "no": 4},
    4: {"pregunta": "¿Puedes entrar al modo recovery desde GRUB? (sí/no)", "si": "sol_fsck", "no": "sol_critico"}
}

soluciones_boot = {
    "sol_grub": "Parece que GRUB no aparece.\nSolución:\n1. Arranca desde un USB Live.\n2. Ejecuta:\n   sudo grub-install /dev/sda\n   sudo update-grub\n3. Reinicia el sistema.",
    "sol_kernel": "El kernel no está cargando.\nSolución:\n1. En el menú GRUB presiona 'e'.\n2. Elimina 'quiet splash'.\n3. Inicia de nuevo para ver errores.\n4. Si falla, reinstala el kernel:\n   sudo apt install --reinstall linux-image-generic",
    "sol_grafico": "El kernel carga pero la pantalla negra indica un problema del entorno gráfico.\nSolución:\n1. Entra en modo texto con Ctrl+Alt+F3.\n2. Reinstala el entorno gráfico:\n   sudo apt install --reinstall ubuntu-desktop\n3. Reinicia:\n   sudo reboot",
    "sol_fsck": "Perfecto, podemos reparar desde recovery.\nEjecuta:\nsudo fsck -f /\nAl terminar, reinicia el sistema.",
    "sol_critico": "No puedes acceder a recovery. Es muy probable que el sistema esté corrupto.\nSolución:\n1. Arranca con un USB Live.\n2. Respalda tus archivos.\n3. Reinstala Linux."
}

# --- Diagnóstico: WiFi no conecta (wifi) ---
diagnostico_wifi = {
    1: {"pregunta": "¿Ves redes WiFi disponibles al listar con 'nmcli dev wifi list'? (sí/no)", "si": 2, "no": "sol_driver_wifi"},
    2: {"pregunta": "¿La interfaz WiFi aparece y está activa (ip link o 'nmcli dev' la muestran UP)? (sí/no)", "si": 3, "no": "sol_activar_wifi"},
    3: {"pregunta": "¿Puedes conectarte a otra red (por ejemplo hotspot del móvil)? (sí/no)", "si": "sol_router", "no": 4},
    4: {"pregunta": "Al conectar, ¿recibes IP (ip addr muestra 'inet' en wlan)? (sí/no)", "si": "sol_dns", "no": "sol_dhcp"}
}

soluciones_wifi = {
    "sol_driver_wifi": "No se ven redes, puede be driver o RFKill.\nPasos:\n1) rfkill list -> sudo rfkill unblock all\n2) lspci/lsusb y firmware\n3) Reinicia NetworkManager",
    "sol_activar_wifi": "La interfaz no está UP.\nPasos:\n1) ip link set wlan0 up\n2) nmcli r wifi on\n3) nmcli dev set wlan0 managed yes",
    "sol_router": "El problema parece ser el router/red específica.\nPasos:\n1) Reinicia router\n2) Olvida y reconecta con nmcli\n3) Verifica filtrado MAC",
    "sol_dns": "La conexión recibe IP pero no resuelve nombres.\nPasos:\n1) ping 8.8.8.8\n2) nmcli con mod ... ipv4.dns '8.8.8.8 8.8.4.4' ipv4.ignore-auto-dns yes\n3) Reinicia conexión",
    "sol_dhcp": "No recibes IP por DHCP.\nPasos:\n1) sudo dhclient -v wlan0\n2) journalctl -u NetworkManager -b\n3) IP estática temporal y probar gateway"
}

# --- Diagnóstico: Sin audio (audio) ---
diagnostico_audio = {
    1: {"pregunta": "¿Aparecen dispositivos de salida en 'pactl list sinks short'? (sí/no)", "si": 2, "no": "sol_detectar_pulse"},
    2: {"pregunta": "¿Se escucha el test con 'speaker-test -c 2' (o 'paplay /usr/share/sounds/alsa/Front_Center.wav')? (sí/no)", "si": 3, "no": "sol_salidas"},
    3: {"pregunta": "¿Está seleccionada la salida correcta y con volumen suficiente? (sí/no)", "si": "sol_app", "no": "sol_seleccion"}
}

soluciones_audio = {
    "sol_detectar_pulse": "No hay sinks en PulseAudio/PipeWire.\nPasos:\n1) Reinicia servidor de audio\n2) pactl info y pactl list cards short\n3) Si usas ALSA puro, instala PulseAudio/PipeWire",
    "sol_salidas": "No se escucha el test.\nPasos:\n1) alsamixer (F6 y volumen)\n2) pavucontrol (Configuration/Output)\n3) pactl set-sink-mute @DEFAULT_SINK@ toggle",
    "sol_seleccion": "Selecciona la salida adecuada.\nPasos:\n1) pactl set-default-sink <NOMBRE>\n2) pactl move-sink-input ...\n3) Probar audio",
    "sol_app": "Si el sistema suena, puede ser la app.\nPasos:\n1) Revisa configuración de la app\n2) Prueba otro archivo/formato\n3) Reinstala/actualiza la app"
}

# --- Diagnóstico: Temperatura/Overheating (temp) ---
diagnostico_temp = {
    1: {"pregunta": "¿Las temperaturas superan 85°C (sensors/powertop)? (sí/no)", "si": 2, "no": 3},
    2: {"pregunta": "¿El equipo es una laptop? (sí/no)", "si": "sol_laptop_temp", "no": "sol_desktop_temp"},
    3: {"pregunta": "¿Algún proceso usa >80% CPU sostenido (htop/top)? (sí/no)", "si": "sol_proceso_cpu", "no": "sol_tp_tuning"}
}

soluciones_temp = {
    "sol_laptop_temp": "Laptop con sobretemperatura.\nPasos:\n1) Limpia polvo y verifica ventilación\n2) Cambia pasta térmica si es antigua\n3) Instala TLP: sudo apt install tlp && sudo tlp start\n4) Revisa powertop y reduce consumo",
    "sol_desktop_temp": "Desktop con sobretemperatura.\nPasos:\n1) Limpia polvo, mejora flujo de aire (ventiladores)\n2) Cambia pasta térmica\n3) Ajusta curvas de ventilador en BIOS o fancontrol",
    "sol_proceso_cpu": "Proceso consumiendo CPU excesiva.\nPasos:\n1) Identifica con htop/top\n2) Limita con nice/renice o corrige el programa\n3) Considera ionice para limitar IO",
    "sol_tp_tuning": "Temperaturas normales, pero molestan ventiladores.\nPasos:\n1) Optimiza TLP/powertop\n2) Ajusta governor de CPU a powersave\n3) Verifica que no haya polvo o obstrucciones"
}

# --- Diagnóstico: Disco lleno/espacio (espacio) ---
diagnostico_espacio = {
    1: {"pregunta": "¿df -h muestra la partición raíz (/) >95%? (sí/no)", "si": 2, "no": 3},
    2: {"pregunta": "¿journalctl muestra logs creciendo mucho? (sí/no)", "si": "sol_logs", "no": 4},
    3: {"pregunta": "¿La partición /home está llena? (sí/no)", "si": "sol_home", "no": "sol_tmp_snap"},
    4: {"pregunta": "¿Tienes muchos kernels viejos instalados? (sí/no)", "si": "sol_kernels", "no": "sol_cache"}
}

soluciones_espacio = {
    "sol_logs": "Limpia logs: sudo journalctl --vacuum-time=7d (o --vacuum-size=200M). Revisa /var/log/*.",
    "sol_home": "Limpia /home: 'ncdu ~' o 'du -sh ~/* | sort -h'. Mueve archivos grandes a otro disco.",
    "sol_tmp_snap": "Limpia temporales y snaps: 'sudo rm -rf /tmp/*' (con cuidado), 'snap list --all' y 'sudo snap remove --purge' versiones antiguas.",
    "sol_kernels": "Elimina kernels viejos: 'dpkg --list | grep linux-image'; 'sudo apt remove linux-image-VERSION' (no elimines el actual).",
    "sol_cache": "Limpia caché: 'sudo apt clean && sudo apt autoremove'. Limpia caches de navegadores y miniaturas."
}

# --- Diagnóstico: APT roto/paquetes (apt) ---
diagnostico_apt = {
    1: {"pregunta": "¿Ves 'dpkg was interrupted' o similar? (sí/no)", "si": "sol_dpkg_config", "no": 2},
    2: {"pregunta": "¿El error dice dependencias no satisfechas? (sí/no)", "si": "sol_fix_deps", "no": 3},
    3: {"pregunta": "¿El error indica claves o repositorios inválidos? (sí/no)", "si": "sol_repos", "no": "sol_reintentar"}
}

soluciones_apt = {
    "sol_dpkg_config": "Completa dpkg: 'sudo dpkg --configure -a' y luego 'sudo apt -f install'.",
    "sol_fix_deps": "Arregla dependencias: 'sudo apt -f install' o intenta 'sudo apt install --reinstall paquete'.",
    "sol_repos": "Revisa /etc/apt/sources.list y .d/. Importa claves faltantes y desactiva repos rotos. Ejecuta 'sudo apt update'.",
    "sol_reintentar": "Intenta: 'sudo apt update && sudo apt upgrade'. Si persiste, 'sudo apt clean' y reintenta."
}

# --- Diagnóstico: Bluetooth no conecta (bluetooth) ---
diagnostico_bluetooth = {
    1: {"pregunta": "¿El adaptador aparece y está encendido (bluetoothctl: power on)? (sí/no)", "si": 2, "no": "sol_bt_power"},
    2: {"pregunta": "¿El dispositivo está emparejado (bluetoothctl: paired-devices)? (sí/no)", "si": 3, "no": "sol_bt_pair"},
    3: {"pregunta": "¿Se conecta pero sin audio o se desconecta al instante? (sí/no)", "si": "sol_bt_profiles", "no": "sol_bt_connect"}
}

soluciones_bluetooth = {
    "sol_bt_power": "Enciende y desbloquea bluetooth.\nPasos:\n1) rfkill list -> rfkill unblock bluetooth\n2) bluetoothctl: power on\n3) Reinicia servicio: sudo systemctl restart bluetooth",
    "sol_bt_pair": "Empareja desde bluetoothctl.\nPasos:\n1) scan on -> pair MAC -> trust MAC -> connect MAC\n2) Si falla, elimina ('remove MAC') y repite",
    "sol_bt_profiles": "Perfiles de audio.\nPasos:\n1) Instala módulos: pulseaudio-module-bluetooth o PipeWire\n2) pavucontrol: selecciona perfil A2DP\n3) Reconecta el dispositivo",
    "sol_bt_connect": "Conexión básica.\nPasos:\n1) bluetoothctl: connect MAC\n2) Verifica controladores y compatibilidad\n3) Revisa logs: journalctl -u bluetooth"
}

# --- Diagnóstico: Impresora no imprime (impresora) ---
diagnostico_impresora = {
    1: {"pregunta": "¿El servicio CUPS está activo? (sí/no)", "si": 2, "no": "sol_cups"},
    2: {"pregunta": "¿La impresora aparece en 'lpstat -p -d'? (sí/no)", "si": 3, "no": "sol_agregar_impresora"},
    3: {"pregunta": "¿La cola tiene trabajos atascados? (sí/no)", "si": "sol_cola", "no": "sol_driver_ppd"}
}

soluciones_impresora = {
    "sol_cups": "Inicia CUPS: 'sudo systemctl enable --now cups'. Revisa http://localhost:631",
    "sol_agregar_impresora": "Agrega impresora desde http://localhost:631 o 'lpadmin'. Conecta y detecta drivers apropiados.",
    "sol_cola": "Cancela trabajos: 'cancel -a'. Reinicia CUPS: 'sudo systemctl restart cups'",
    "sol_driver_ppd": "Reinstala/selecciona el PPD correcto. 'apt install printer-driver-all' puede ayudar. Imprime página de prueba"
}

# --- Diagnóstico: Sistema lento / rendimiento (lento) ---
diagnostico_lento = {
    1: {"pregunta": "¿La CPU está al 100% sostenida (htop/top)? (sí/no)", "si": "sol_cpu", "no": 2},
    2: {"pregunta": "¿La RAM está casi llena y hay mucho swap? (sí/no)", "si": "sol_mem", "no": 3},
    3: {"pregunta": "¿El disco muestra alto IO wait (iostat/iotop)? (sí/no)", "si": "sol_io", "no": "sol_general"}
}

soluciones_lento = {
    "sol_cpu": "CPU saturada.\nPasos:\n1) Identifica proceso: htop/top\n2) Limita con nice/renice\n3) Revisa actualizaciones o bugs de la app",
    "sol_mem": "Memoria escasa.\nPasos:\n1) Cierra apps pesadas\n2) Aumenta swap (swapfile)\n3) Considera ampliar RAM",
    "sol_io": "IO de disco alto.\nPasos:\n1) Revisa procesos con iotop\n2) Usa ionice para cargas en background\n3) Verifica salud del disco (smartctl)",
    "sol_general": "Optimización general.\nPasos:\n1) Desactiva servicios innecesarios\n2) Limpia arranque de sesiones\n3) Actualiza sistema y drivers"
}

# --- Diagnóstico: Nginx no arranca / 502/504 (nginx) ---
# Meta: distinguir entre servicio caído, config inválida, puerto ocupado, o upstream caído (502/504)

diagnostico_nginx = {
    1: {"pregunta": "¿El servicio nginx está activo? ('systemctl is-active nginx') (sí/no)", "si": 2, "no": "sol_nginx_start"},
    2: {"pregunta": "¿La prueba de configuración 'nginx -t' pasa sin errores? (sí/no)", "si": 3, "no": "sol_nginx_config"},
    3: {"pregunta": "¿El puerto 80/443 está libre para nginx? ('ss -tuln | grep :80') (sí/no)", "si": 4, "no": "sol_nginx_puerto"},
    4: {"pregunta": "¿Ves errores 502/504 en los logs de nginx? (sí/no)", "si": "sol_nginx_upstream", "no": "sol_nginx_logs"}
}

soluciones_nginx = {
    "sol_nginx_start": "Servicio caído.\nPasos:\n1) Inicia: sudo systemctl start nginx\n2) Habilita al arranque: sudo systemctl enable nginx\n3) Revisa estado: systemctl status nginx",
    "sol_nginx_config": "Configuración inválida.\nPasos:\n1) Revisa '/etc/nginx/nginx.conf' y sites-enabled\n2) Corrige errores reportados por 'sudo nginx -t'\n3) Recarga: sudo systemctl reload nginx",
    "sol_nginx_puerto": "Puerto ocupado.\nPasos:\n1) Identifica proceso: sudo lsof -i :80 o ss -tulnp | grep :80\n2) Cambia/ajusta el otro servicio o el puerto en nginx\n3) Reinicia: sudo systemctl restart nginx",
    "sol_nginx_upstream": "Errores 502/504 (backend caído).\nPasos:\n1) Verifica upstream (app) está arriba y escucha (e.g., 127.0.0.1:3000)\n2) Comprueba proxy_pass en el server block\n3) Revisa timeouts: proxy_read_timeout, proxy_connect_timeout\n4) Reinicia backend y luego reload nginx",
    "sol_nginx_logs": "Revisar logs.\nPasos:\n1) Error log: /var/log/nginx/error.log\n2) Access log: /var/log/nginx/access.log\n3) Ajusta configuración según errores y 'sudo systemctl reload nginx'"
}
