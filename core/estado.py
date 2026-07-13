# ==========================================
# Estado global de la conversión
# ==========================================

cancelar = False


def detener():

    global cancelar

    cancelar = True


def reiniciar():

    global cancelar

    cancelar = False


def detenido():

    return cancelar 