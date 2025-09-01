/**
 * Script principal para la interfaz del compilador FlashML
 */
document.addEventListener("DOMContentLoaded", function () {
  // Configurar el editor con CodeMirror
  const editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    mode: "text/x-flashml",
    lineNumbers: true,
    indentUnit: 4,
    theme: localStorage.getItem("theme") === "light" ? "eclipse" : "default",
    autoCloseTags: true,
  });

  // Código de ejemplo por defecto
  editor.setValue(`@velocista
    @titulo La velocidad de Barry Allen @/titulo
    
    @temporada numero="1"
        @episodio
            @titulo El hombre más rápido @/titulo
            @escena
                @personaje nombre="Barry Allen" actor="Grant Gustin"
                    @dialogo
                        ¡Soy @rapido el hombre más rápido @/rapido del mundo!
                    @/dialogo
                    @accion velocidad="máxima"
                        Barry corre a través de Central City.
                    @/accion
                @/personaje
            @/escena
            @villanos
                @villano nombre="Reverse Flash" poder="Super velocidad"
                    El enemigo jurado de Flash.
                @/villano
            @/villanos
        @/episodio
    @/temporada
    
    @imagen src="flash.jpg" alt="Barry Allen corriendo" @/imagen
    
    ## Comentario: Escena de acción rápida ##
@/velocista`);

  // Cargar tema desde localStorage
  const savedTheme = localStorage.getItem("theme") || "dark";
  document.body.className = `theme-${savedTheme} min-h-screen flex flex-col bg-[url('data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'60\\' height=\\'60\\' viewBox=\\'0 0 60 60\\'><path d=\\'M30 5 L35 25 L45 25 L35 35 L40 55 L30 40 L20 55 L25 35 L15 25 L25 25 Z\\' stroke=\\'%23cc0000\\' stroke-width=\\'0.5\\' fill=\\'none\\' opacity=\\'0.03\\'/></svg>')] bg-fixed`;
  const themeIcon = document.getElementById("theme-icon");
  themeIcon.innerHTML =
    savedTheme === "light"
      ? `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>`
      : `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>`;

  // Cambiar tema
  document.getElementById("theme-toggle").addEventListener("click", () => {
    const currentTheme = document.body.classList.contains("theme-dark")
      ? "dark"
      : "light";
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    document.body.classList.remove(`theme-${currentTheme}`);
    document.body.classList.add(`theme-${newTheme}`);
    localStorage.setItem("theme", newTheme);
    editor.setOption("theme", newTheme === "light" ? "eclipse" : "default");
    themeIcon.innerHTML =
      newTheme === "light"
        ? `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>`
        : `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>`;
  });

  // Abrir documentación
  document.getElementById("help-button").addEventListener("click", () => {
    window.open("/documentation", "_blank");
  });

  // Indentación automática con Ctrl + S
  document.addEventListener("keydown", function (e) {
    if (e.ctrlKey && e.key === "s") {
      e.preventDefault();
      editor.execCommand("indentAuto");
      const estado = document.getElementById("estado");
      estado.innerHTML = "> Código formateado automáticamente";
      setTimeout(() => {
        estado.innerHTML = "> Sistema listo para compilar código FlashML...";
      }, 3000);
    }
  });

  // Compilar el código
  document.getElementById("compilar").addEventListener("click", async () => {
    const codigo = editor.getValue();
    const estado = document.getElementById("estado");
    const compartirBtn = document.getElementById("compartir");

    estado.innerHTML = "> Compilando código FlashML a HTML...";
    compartirBtn.style.display = "none";

    try {
      const response = await fetch("/compilar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codigo }),
      });
      const data = await response.json();

      if (data.success) {
        estado.innerHTML = `> <span class="text-green-400">Compilación exitosa.</span> El archivo HTML generado está disponible en el panel "Archivos Generados".`;
        compartirBtn.style.display = "inline-flex";
        // Actualizar archivos generados
        actualizarArchivosGenerados(data.html_path);
      } else {
        estado.innerHTML =
          "> <span class='text-red-500'>Errores de compilación:</span><br>" +
          data.errores
            .map((e) => `> [${e.tipo.toUpperCase()}] ${e.mensaje}`)
            .join("<br>");
      }
    } catch (e) {
      estado.innerHTML = `> <span class="text-red-500">Error de conexión:</span> ${e.message}`;
    }
  });

  // Compartir el código (simulado)
  document.getElementById("compartir").addEventListener("click", () => {
    alert(
      "Función de compartir no implementada. Requiere backend para generar enlaces compartibles."
    );
  });

  // Limpiar estado
  document.getElementById("limpiar-estado").addEventListener("click", () => {
    document.getElementById("estado").innerHTML =
      "> Sistema listo para compilar código FlashML...";
    document.getElementById("compartir").style.display = "none";
  });

  // Toggle para la referencia rápida
  document.getElementById("quick-ref-header").addEventListener("click", () => {
    const content = document.getElementById("quick-ref-content");
    const icon = document.getElementById("quick-ref-icon");
    content.classList.toggle("hidden");
    icon.classList.toggle("transform");
    icon.classList.toggle("rotate-180");
  });

  // Función para actualizar la lista de archivos generados
  async function actualizarArchivosGenerados(nuevoArchivo) {
    try {
      const response = await fetch("/archivos");
      const data = await response.json();
      if (data.archivos) {
        const contenedor = document.getElementById("archivos-generados");
        contenedor.innerHTML = data.archivos
          .map(
            (archivo) => `
                    <div class="file-card bg-black bg-opacity-30 rounded-md border border-flash-gray border-opacity-50 transition-all duration-300 overflow-hidden">
                        <div class="px-3 py-2 flex justify-between items-center">
                            <div class="flex items-center space-x-2">
                                <i class="fas fa-file-code text-flash-yellow"></i>
                                <span class="text-sm font-medium">${
                                  archivo.nombre
                                }</span>
                            </div>
                            <span class="text-xs text-gray-400">${new Date(
                              archivo.fecha
                            ).toLocaleDateString()}</span>
                        </div>
                        <div class="px-3 pb-2 text-xs text-gray-400 flex justify-between">
                            <span>${archivo.tamano}</span>
                            <div class="flex space-x-2">
                                <button class="text-flash-yellow hover:text-flash-gold transition-colors view-btn" title="Ver" data-path="/output/${
                                  archivo.nombre
                                }">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="text-flash-yellow hover:text-flash-gold transition-colors download-btn" title="Descargar" data-path="${
                                  archivo.path
                                }">
                                    <i class="fas fa-download"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                `
          )
          .join("");

        // Agregar eventos a los botones de ver y descargar
        const viewButtons = contenedor.querySelectorAll(".view-btn");
        viewButtons.forEach((button) => {
          button.addEventListener("click", () => {
            const path = button.getAttribute("data-path");
            window.open(path, "_blank");
          });
        });

        const downloadButtons = contenedor.querySelectorAll(".download-btn");
        downloadButtons.forEach((button) => {
          button.addEventListener("click", () => {
            const path = button.getAttribute("data-path");
            descargarArchivo(path);
          });
        });

        // Actualizar contador de archivos
        document.getElementById(
          "contador-archivos"
        ).textContent = `${data.archivos.length} archivos`;
      }
    } catch (e) {
      console.error("Error al actualizar archivos generados:", e);
    }
  }

  // Función para descargar archivo
  function descargarArchivo(path) {
    const a = document.createElement("a");
    a.href = `/static/${path}`;
    a.download = path.split("/").pop();
    a.click();
  }

  // Cargar archivos generados al iniciar
  actualizarArchivosGenerados();
});
