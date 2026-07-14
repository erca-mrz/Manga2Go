import os
import sys


def recurso(ruta_relativa):

    if getattr(sys, "frozen", False):

        base = sys._MEIPASS

    else:

        base = os.path.abspath(".")

    return os.path.join(base, ruta_relativa)
