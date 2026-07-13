import os
import re


FORMATOS_IMAGEN = (
    ".webp",
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tiff",
    ".gif",
    ".avif"
)



def analizar_carpeta(ruta):

    total_carpetas = 0
    total_imagenes = 0

    elementos = os.listdir(ruta)

    hay_imagenes = any(
        es_imagen(archivo)
        for archivo in elementos
    )

    if hay_imagenes:

        total_imagenes = len(
            [
                archivo
                for archivo in elementos
                if es_imagen(archivo)
            ]
        )

    else:

        for carpeta in elementos:

            ruta_carpeta = os.path.join(
                ruta,
                carpeta
            )

            if os.path.isdir(ruta_carpeta):

                total_carpetas += 1

                total_imagenes += len(

                    [

                        archivo

                        for archivo in os.listdir(ruta_carpeta)

                        if es_imagen(archivo)

                    ]

                )

    return (
        total_carpetas,
        total_imagenes
    )


def es_imagen(nombre):

    return nombre.lower().endswith(
        FORMATOS_IMAGEN
    )


def obtener_numero(nombre):

    nombre = os.path.splitext(nombre)[0]

    patron = r"(\d+(?:\.\d+)?)$"

    coincidencia = re.search(
        patron,
        nombre
    )

    if coincidencia:
        return float(
            coincidencia.group(1)
        )

    return float("inf")

# ==========================================
# Comparar capítulos con PDFs existentes
# ==========================================

def comparar_capitulos(origen, destino):

    if not origen or not destino:
        return [], [], []

    carpetas = [

        carpeta

        for carpeta in os.listdir(origen)

        if os.path.isdir(
            os.path.join(origen, carpeta)
        )

    ]

    pdfs = [

        os.path.splitext(pdf)[0]

        for pdf in os.listdir(destino)

        if pdf.lower().endswith(".pdf")

    ]

    existentes = [
        carpeta
        for carpeta in carpetas
        if carpeta in pdfs
    ]

    pendientes = [
        carpeta
        for carpeta in carpetas
        if carpeta not in pdfs
    ]

    resultado = {

    "carpetas": carpetas,

    "existentes": existentes,

    "pendientes": pendientes,

    "cantidad_pdfs": len(existentes)

    }

    return resultado

