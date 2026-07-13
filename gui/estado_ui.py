# ==========================================
# ESTADOS DE LA INTERFAZ
# ==========================================

def inicio(label):
    label.configure(text="📂 Selecciona una carpeta de origen")


def destino(label):
    label.configure(text="📁 Selecciona una carpeta de destino")


def listo(label):
    label.configure(text="🚀 Listo para convertir")


def convirtiendo(label):
    label.configure(text="📖 Convirtiendo...")


def finalizado(label):
    label.configure(text="🎉 Conversión finalizada")


def cancelado(label):
    label.configure(text="⛔ Conversión cancelada")