import os

from PIL import Image

import core.estado as estado

from core.utils import (
    obtener_numero,
    es_imagen
)

from gui.logs import (
    log_inicio,
    log_procesando,
    log_capitulo,
    log_error,
    log_final
)


# ==========================================
# Conversión principal
# ==========================================
def convertir(

    origen,
    salida,
    escribir_log,
    actualizar_progreso,
    reemplazar

):

    log_inicio(

        escribir_log,
        origen,
        salida

    )

    carpetas = obtener_carpetas(origen)

    convertir_carpetas(

        carpetas,

        salida,

        escribir_log,

        actualizar_progreso,

        reemplazar

    )

    if estado.detenido():

        escribir_log("")
        escribir_log("⛔ Conversión cancelada.")

    else:

        log_final(
            escribir_log
        )
# ==========================================
# Obtener una carpetaS
# ==========================================

def obtener_carpetas(origen):

    elementos = sorted(

        os.listdir(origen),

        key=obtener_numero

    )

    hay_imagenes = any(

        es_imagen(archivo)

        for archivo in elementos

    )

    if hay_imagenes:

        return [origen]

    return [

        os.path.join(origen, carpeta)

        for carpeta in elementos

        if os.path.isdir(

            os.path.join(

                origen,

                carpeta

            )

        )

    ]

def convertir_carpetas(

    carpetas,

    salida,

    escribir_log,

    actualizar_progreso,

    reemplazar

):

    total = len(carpetas)

    for indice, ruta_carpeta in enumerate(

        carpetas,

        start=1

    ):

        if estado.detenido():

            return

        convertir_carpeta(

            ruta_carpeta,

            salida,

            escribir_log,

            reemplazar

        )

        actualizar_progreso(

            indice,

            total

        )

# ==========================
# CONVERTIR LISTA
# ==========================

def convertir_lista(

    carpetas,

    salida,

    escribir_log,

    actualizar_progreso,

    reemplazar

):

    total = len(carpetas)

    for indice, ruta_carpeta in enumerate(

        carpetas,

        start=1

    ):

        if estado.detenido():

            escribir_log(
                "⛔ Conversión cancelada."
            )

            return

        convertir_carpeta(

            ruta_carpeta,

            salida,

            escribir_log,

            reemplazar

        )

        actualizar_progreso(

            indice,

            total

        )


# ==========================
# CONVERTIR CARPETA
# ==========================

def convertir_carpeta(

    ruta_carpeta,

    salida,

    escribir_log,

    reemplazar

):

    imagenes = obtener_imagenes(

        ruta_carpeta

    )

    log_procesando(

        escribir_log,

        os.path.basename(ruta_carpeta),

        len(imagenes)

    )

    if not imagenes:

        log_error(

            escribir_log,

            "No se encontraron imágenes."

        )

        return

    imagenes_pil = cargar_imagenes(

        ruta_carpeta,

        imagenes,

        escribir_log

    )

    guardar_pdf(

        ruta_carpeta,

        salida,

        imagenes_pil,

        len(imagenes),

        escribir_log,

        reemplazar

    )

# ==========================
# OBTENER IMÁGENES
# ==========================
def obtener_imagenes(

    ruta_carpeta

):

    return sorted(

        [

            archivo

            for archivo in os.listdir(

                ruta_carpeta

            )

            if es_imagen(

                archivo

            )

        ],

        key=obtener_numero

    )

# ==========================
# CARGAR IMÁGENES
# ==========================

def cargar_imagenes(

    ruta_carpeta,

    imagenes,

    escribir_log

):

    imagenes_pil = []

    for imagen in imagenes:

        if estado.detenido():

            log_error(

                escribir_log,

                "Conversión cancelada."

            )

            return []

        ruta = os.path.join(

            ruta_carpeta,

            imagen

        )

        try:

            img = Image.open(ruta)

            img = img.convert("RGB")

            imagenes_pil.append(

                img

            )

        except Exception as e:

            log_error(

                escribir_log,

                f"No se pudo abrir {imagen}: {e}"

            )

    return imagenes_pil

# ==========================
# GUARDAR PDF
# ==========================

def obtener_nombre_pdf(ruta_carpeta):

    return (

        os.path.basename(

            ruta_carpeta

        )

        + ".pdf"

    )

def guardar_pdf(

    ruta_carpeta,

    salida,

    imagenes_pil,

    cantidad,

    escribir_log,

    reemplazar

):

    # ==========================
    # No hay imágenes válidas
    # ==========================

    if not imagenes_pil:

        log_error(

            escribir_log,

            "No se pudo convertir ninguna imagen."

        )

        return


    # ==========================
    # Nombre del PDF
    # ==========================

    nombre_pdf = obtener_nombre_pdf(ruta_carpeta)

    ruta_pdf = os.path.join(

    salida,

    nombre_pdf

    )

    ruta_pdf = os.path.join(

        salida,

        nombre_pdf

    )


    # ==========================
    # ¿Cancelar antes de guardar?
    # ==========================

    if estado.detenido():

        escribir_log("")

        escribir_log("⛔ Conversión cancelada.")

        return


    # ==========================
    # Ya existe
    # ==========================

    if os.path.exists(ruta_pdf):

        if not reemplazar:

            escribir_log("")

            escribir_log(

                f"⏭ PDF existente: {nombre_pdf}"

            )

            escribir_log(

                "   Se omitió la conversión."

            )

            return

        escribir_log("")

        escribir_log(

            f"♻ Reemplazando: {nombre_pdf}"

        )


    # ==========================
    # Guardar PDF
    # ==========================

    imagenes_pil[0].save(

        ruta_pdf,

        save_all=True,

        append_images=imagenes_pil[1:]

    )


    # ==========================
    # Log final
    # ==========================

    log_capitulo(

        escribir_log,

        os.path.basename(

            ruta_carpeta

        ),

        cantidad,

        nombre_pdf,

        salida

    )