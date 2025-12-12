# diagnosticos.py
# Motor experto de diagnóstico para "Linux no arranca"

diagnostico_boot = {
    1: {
        "pregunta": "¿Ves el menú de GRUB al encender la computadora? (sí/no)",
        "si": 2,
        "no": "sol_grub"
    },
    2: {
        "pregunta": "Después de seleccionar tu sistema, ¿ves texto cargando antes de que falle? (sí/no)",
        "si": 3,
        "no": "sol_kernel"
    },
    3: {
        "pregunta": "¿La pantalla se queda completamente negra después de cargar el kernel? (sí/no)",
        "si": "sol_grafico",
        "no": 4
    },
    4: {
        "pregunta": "¿Puedes entrar al modo recovery desde GRUB? (sí/no)",
        "si": "sol_fsck",
        "no": "sol_critico"
    }
}

# Soluciones finales
soluciones_boot = {
    "sol_grub":
        "Parece que GRUB no aparece.\n"
        "Solución:\n"
        "1. Arranca desde un USB Live.\n"
        "2. Ejecuta:\n"
        "   sudo grub-install /dev/sda\n"
        "   sudo update-grub\n"
        "3. Reinicia el sistema.",
    
    "sol_kernel":
        "El kernel no está cargando.\n"
        "Solución:\n"
        "1. En el menú GRUB presiona 'e'.\n"
        "2. Elimina 'quiet splash'.\n"
        "3. Inicia de nuevo para ver errores.\n"
        "4. Si falla, reinstala el kernel:\n"
        "   sudo apt install --reinstall linux-image-generic",

    "sol_grafico":
        "El kernel carga pero la pantalla negra indica un problema del entorno gráfico.\n"
        "Solución:\n"
        "1. Entra en modo texto con Ctrl+Alt+F3.\n"
        "2. Reinstala el entorno gráfico:\n"
        "   sudo apt install --reinstall ubuntu-desktop\n"
        "3. Reinicia:\n"
        "   sudo reboot",

    "sol_fsck":
        "Perfecto, podemos reparar desde recovery.\n"
        "Ejecuta:\n"
        "sudo fsck -f /\n"
        "Al terminar, reinicia el sistema.",

    "sol_critico":
        "No puedes acceder a recovery. Es muy probable que el sistema esté corrupto.\n"
        "Solución:\n"
        "1. Arranca con un USB Live.\n"
        "2. Respalda tus archivos.\n"
        "3. Reinstala Linux."
}
