# ==========================================
# Separador
# ==========================================



def log_separador(escribir_log):

    escribir_log(
        "════════════════════════════════════════"
    )


# ==========================================
# Inicio de conversión
# ==========================================

def log_inicio(
    escribir_log,
    origen,
    salida
):

    log_separador(escribir_log)

    escribir_log("🚀 Iniciando conversión")
    escribir_log("")
    escribir_log(f"📂 Origen : {origen}")
    escribir_log(f"📁 Destino: {salida}")

    log_separador(escribir_log)


# ==========================================
# Capítulo
# ==========================================

def log_capitulo(
    escribir_log,
    nombre_capitulo,
    cantidad_imagenes,
    nombre_pdf,
    destino
):

    log_separador(escribir_log)

    escribir_log(f"📂 {nombre_capitulo}")

    escribir_log(
        f"   🖼 Imágenes : {cantidad_imagenes}"
    )

    escribir_log(
        f"   📄 PDF      : {nombre_pdf}"
    )

    escribir_log(
        f"   📁 Destino  : {destino}"
    )

    escribir_log("")

    escribir_log(
        "   ✅ Conversión completada"
    )


# ==========================================
# Error
# ==========================================

def log_error(
    escribir_log,
    mensaje
):

    escribir_log(
        f"⚠ {mensaje}"
    )


# ==========================================
# Final
# ==========================================

def log_final(escribir_log):

    log_separador(escribir_log)

    escribir_log(
        "🎉 Conversión finalizada."
    )

    log_separador(escribir_log)

def log_resumen_origen(

    escribir_log,

    ruta,

    carpetas,

    imagenes

):

    log_separador(escribir_log)

    escribir_log("📂 Carpeta origen")

    escribir_log("")

    escribir_log(ruta)

    escribir_log("")

    if carpetas:

        escribir_log(

            f"📚 Capítulos encontrados: {carpetas}"

        )

    escribir_log(

        f"🖼 Imágenes encontradas: {imagenes}"

    )

    if imagenes and carpetas == 0:

        escribir_log("")

        escribir_log("📄 Se generará un único PDF.")

    escribir_log("")

    escribir_log("✅ Origen listo.")

def log_resumen_destino(

    escribir_log,

    ruta,

    cantidad_pdfs

):

    log_separador(escribir_log)

    escribir_log("📁 Carpeta destino")

    escribir_log("")

    escribir_log(ruta)

    escribir_log("")

    escribir_log(

        f"📄 PDFs encontrados: {cantidad_pdfs}"

    )

    escribir_log("")

    escribir_log("✅ Destino listo.")


def log_procesando(

    escribir_log,

    nombre,

    cantidad
):

        log_separador(escribir_log)

        escribir_log("⏳ Procesando")

        escribir_log("")

        escribir_log(f"📂 {nombre}")

        escribir_log(f"🖼 {cantidad} imágenes")

        escribir_log("")



def log_comparacion(
    escribir_log,
    carpetas,
    existentes,
    pendientes
):

    log_separador(escribir_log)

    escribir_log("📄 Comparando con carpeta destino")
    escribir_log("")

    if len(existentes) == 0:

        escribir_log(
            "No existen PDFs."
        )

        escribir_log(
            f"🆕 Se convertirán {len(pendientes)} capítulos."
        )

    elif len(pendientes) == 0:

        escribir_log(
            "✔ Todos los capítulos ya existen."
        )

        escribir_log(
            "No hay nada que convertir."
        )

    else:

        escribir_log(
            f"✔ Ya existen: {len(existentes)}"
        )

        escribir_log(
            f"🆕 Se convertirán: {len(pendientes)}"
        )

    log_separador(escribir_log)

