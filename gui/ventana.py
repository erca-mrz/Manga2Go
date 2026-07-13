import customtkinter as ctk

from tkinter import filedialog

from threading import Thread

from core.converter import convertir

from core.control import (
    detener,
    reiniciar
)

from core.utils import (
    analizar_carpeta,
    comparar_capitulos
)

from gui.logs import (
    log_resumen_origen,
    log_resumen_destino,
    log_comparacion
)

from gui import estado_ui

from core import estado
from core.estado import detener

from gui.ui import UI

ANCHO_VENTANA = 900
ALTO_VENTANA = 600


# ==========================
# FUNCIONES AUXILIARES
# ==========================

def escribir_log(log, texto):

    texto = str(texto)

    print(texto)

    log.insert("end", texto + "\n")
    log.see("end")

def actualizar_progreso(
    barra,
    lbl_estado,
    actual,
    total
):

    if total > 0:

        barra.set(actual / total)

    lbl_estado.configure(
        text=f"📚 {actual} / {total} capítulos"
    )


def actualizar_estado(

    ui,

    convirtiendo=False

):

    origen = ui.entry_origen.get()
    salida = ui.entry_salida.get()

    if convirtiendo:

        estado_ui.convirtiendo(ui.lbl_estado)

        ui.btn_convertir.configure(state="disabled")
        ui.btn_detener.configure(state="normal")

        return

    if not origen:

        estado_ui.inicio(ui.lbl_estado)

        ui.btn_convertir.configure(state="disabled")
        ui.btn_detener.configure(state="disabled")

    elif not salida:

        estado_ui.destino(ui.lbl_estado)

        ui.btn_convertir.configure(state="disabled")
        ui.btn_detener.configure(state="disabled")

    else:

        if ui.es_carpeta_simple:

            ui.lbl_estado.configure(

                text="🖼 Carpeta lista para convertir."

            )

            ui.btn_convertir.configure(

                state="normal"

            )
            return

        if ui.pendientes == 0:

            if ui.reemplazar.get():

                ui.lbl_estado.configure(

                    text=f"♻ Se reemplazarán {ui.cantidad_pdfs} PDFs existentes."

                )

                ui.btn_convertir.configure(

                    state="normal"

                )

            else:

                ui.lbl_estado.configure(

                    text="✔ No hay capítulos pendientes."

                )

                ui.btn_convertir.configure(

                    state="disabled"

                )

        else:

            ui.lbl_estado.configure(

                text=f"🚀 {ui.pendientes} capítulos listos para convertir."

            )

            ui.btn_convertir.configure(

                state="normal"

            )

        ui.btn_detener.configure(

            state="disabled"

        )


def actualizar_proyecto(ui):

    origen = ui.entry_origen.get()
    salida = ui.entry_salida.get()

    # Si no hay origen todavía
    if not origen:
        return

    carpetas, imagenes = analizar_carpeta(origen)

    ui.es_carpeta_simple = (

        carpetas == 0

        and

        imagenes > 0

    )

    log_resumen_origen(

            lambda texto: escribir_log(ui.log, texto),

            origen,

            carpetas,

            imagenes

        )
    
     # Si todavía no hay destino
    if not salida:
        return

    resultado = comparar_capitulos(
        origen,
        salida
    )

    ui.pendientes = len(resultado["pendientes"])
    ui.cantidad_pdfs = resultado["cantidad_pdfs"]

    log_resumen_destino(

        lambda texto: escribir_log(ui.log, texto),

        salida,

        resultado["cantidad_pdfs"]
    )

    log_comparacion(

        lambda texto: escribir_log(ui.log, texto),

        resultado["carpetas"],

        resultado["existentes"],

        resultado["pendientes"]

    )


def seleccionar_carpeta(

    entry,

    ui

):

    carpeta = filedialog.askdirectory()

    if not carpeta:
        return

    entry.delete(0, "end")
    entry.insert(0, carpeta)

    actualizar_proyecto(ui)

    actualizar_estado(ui)

def iniciar_conversion(ui):

    estado.reiniciar()

    actualizar_estado(

        ui,

        convirtiendo=True

    )

    def tarea():

        convertir(

            ui.entry_origen.get(),

            ui.entry_salida.get(),

            lambda texto: escribir_log(ui.log, texto),

            lambda actual, total: actualizar_progreso(

                ui.barra,

                ui.lbl_estado,

                actual,

                total

            ),

            ui.reemplazar.get()

        )

        ui.lbl_estado.after(

            0,

            lambda: actualizar_estado(ui)

        )

    Thread(

        target=tarea,

        daemon=True

    ).start()


# ===========================
# CREAR VENTANA
# ===========================

def crear_ventana():

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()

    app.iconbitmap("assets/icon.ico")
    app.title("📄 Manga2Go 1.0")

    app.geometry(
        f"{ANCHO_VENTANA}x{ALTO_VENTANA}"
    )

    app.minsize(
        ANCHO_VENTANA,
        ALTO_VENTANA
    )

    return app


def crear_frame(app):

    frame = ctk.CTkFrame(app)

    frame.pack(

        fill="both",

        expand=True,

        padx=20,

        pady=20

    )

    frame.grid_columnconfigure(

        1,

        weight=1

    )

    frame.grid_rowconfigure(

        4,

        weight=1

    )

    return frame


def crear_titulo(frame):

    titulo = ctk.CTkLabel(

        frame,

        text="📄 Manga2Go 1.0",

        font=("Segoe UI", 24, "bold")

    )

    titulo.grid(

        row=0,

        column=0,

        columnspan=3,

        pady=(10, 25)

    )

# ===========================
# WIDGETS
# ===========================

def crear_log(frame):

    log = ctk.CTkTextbox(

        frame

    )

    log.grid(

        row=4,

        column=0,

        columnspan=3,

        sticky="nsew",

        padx=10,

        pady=10

    )

    return log

def crear_barra(frame):

    barra = ctk.CTkProgressBar(

        frame

    )

    barra.grid(

        row=5,

        column=0,

        columnspan=3,

        sticky="ew",

        padx=10,

        pady=10

    )

    barra.set(0)

    return barra

def crear_estado(frame):

    lbl_estado = ctk.CTkLabel(

        frame,

        text=""

    )

    lbl_estado.grid(

        row=6,

        column=0,

        columnspan=2,

        sticky="w",

        padx=10,

        pady=(0,10)

    )

    return lbl_estado

def crear_checkbox(frame):

    reemplazar = ctk.BooleanVar(

        value=False

    )

    check = ctk.CTkCheckBox(

        frame,

        text="✔ Reemplazar PDFs existentes",

        variable=reemplazar

    )

    check.grid(

        row=3,

        column=0,

        columnspan=3,

        sticky="w",

        padx=10,

        pady=(0,10)

    )

    return check, reemplazar

def crear_selectores(frame):

    ctk.CTkLabel(

        frame,

        text="Carpeta origen:"

    ).grid(

        row=1,

        column=0,

        padx=10,

        pady=10,

        sticky="w"

    )

    entry_origen = ctk.CTkEntry(frame)

    entry_origen.grid(

        row=1,

        column=1,

        sticky="ew",

        padx=10

    )

    btn_origen = ctk.CTkButton(

        frame,

        text="Examinar"

    )

    btn_origen.grid(

        row=1,

        column=2,

        padx=10

    )



    ctk.CTkLabel(

        frame,

        text="Carpeta salida:"

    ).grid(

        row=2,

        column=0,

        padx=10,

        pady=10,

        sticky="w"

    )

    entry_salida = ctk.CTkEntry(frame)

    entry_salida.grid(

        row=2,

        column=1,

        sticky="ew",

        padx=10

    )

    btn_salida = ctk.CTkButton(

        frame,

        text="Examinar"

    )

    btn_salida.grid(

        row=2,

        column=2,

        padx=10

    )

    return (

        entry_origen,

        entry_salida,

        btn_origen,

        btn_salida

    )

def crear_botones(frame):

    btn_convertir = ctk.CTkButton(

        frame,

        text="🚀 Convertir",

        state="disabled"

    )

    btn_convertir.grid(

        row=7,

        column=0,

        pady=15,

        padx=10,

        sticky="w"

    )



    btn_detener = ctk.CTkButton(

        frame,

        text="⛔ Detener",

        state="disabled"

    )

    btn_detener.grid(

        row=7,

        column=2,

        pady=15,

        padx=10,

        sticky="e"

    )

    return (

        btn_convertir,

        btn_detener

    )

def conectar_eventos(ui):

    # ==========================
    # Botón carpeta origen
    # ==========================

    ui.btn_origen.configure(

        command=lambda: seleccionar_carpeta(

            ui.entry_origen,

            ui

        )

    )

    # ==========================
    # Botón carpeta salida
    # ==========================

    ui.btn_salida.configure(

        command=lambda: seleccionar_carpeta(

            ui.entry_salida,

            ui

        )

    )

    # ==========================
    # Botón convertir
    # ==========================

    ui.btn_convertir.configure(

        command=lambda: iniciar_conversion(

            ui

        )

    )

    # ==========================
    # Botón detener
    # ==========================

    ui.btn_detener.configure(

        command=detener
    )

    ui.check_reemplazar.configure(

        command=lambda: (

            actualizar_proyecto(ui),

            actualizar_estado(ui)

        )

    )

def iniciar_aplicacion():

    app = crear_ventana()

    frame = crear_frame(app)

    crear_titulo(frame)

    ui = UI()

    ui.log = crear_log(frame)

    ui.barra = crear_barra(frame)

    ui.lbl_estado = crear_estado(frame)

    (
        ui.entry_origen,
        ui.entry_salida,

        ui.btn_origen,
        ui.btn_salida

    ) = crear_selectores(frame)

    ui.check_reemplazar, ui.reemplazar = crear_checkbox(frame)

    (
        ui.btn_convertir,
        ui.btn_detener

    ) = crear_botones(frame)

    conectar_eventos(ui)

    actualizar_estado(ui)

    app.mainloop()