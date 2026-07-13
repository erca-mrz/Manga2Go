import os

from core.utils import obtener_numero
from core.converter import es_imagen


def analizar_carpeta(ruta):

    resultado = {
        "tipo": "",
        "cantidad_capitulos": 0,
        "cantidad_imagenes": 0,
        "lista": []
    }

    elementos = sorted(
        os.listdir(ruta),
        key=obtener_numero
    )

    hay_imagenes = any(
        es_imagen(elemento)
        for elemento in elementos
    )

    if hay_imagenes:

        resultado["tipo"] = "capitulo"

        resultado["lista"] = [
            archivo
            for archivo in elementos
            if es_imagen(archivo)
        ]

        resultado["cantidad_imagenes"] = len(resultado["lista"])

    else:

        resultado["tipo"] = "coleccion"

        resultado["lista"] = [
            carpeta
            for carpeta in elementos
            if os.path.isdir(os.path.join(ruta, carpeta))
        ]

        resultado["cantidad_capitulos"] = len(resultado["lista"])

    return resultado