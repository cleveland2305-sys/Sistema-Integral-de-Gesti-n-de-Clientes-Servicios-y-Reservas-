import tkinter as tk
from tkinter import ttk, messagebox

# Importamos las clases que ya existen en el archivo soluciontrabajocolaborativo.py
# Cliente: sirve para crear un cliente y validar sus datos (nombre, documento, email, teléfono)
# GestorSoftwareFJ: es el encargado de guardar los clientes en una lista y revisar que no se repitan
# SistemaLogger: guarda los mensajes y errores en un archivo de texto (.log)
# SoftwareFJError: es el error general que lanza el sistema cuando algún dato está mal
from soluciontrabajocolaborativo import (
    Cliente,
    GestorSoftwareFJ,
    SistemaLogger,
    SoftwareFJError,
)

# joharuiz0940@gmail.com 


# ==============================================================================
# 1. CONEXIÓN CON LA LÓGICA DEL SISTEMA (BACKEND)
# ==============================================================================
# Creamos el logger para que todo lo que pase se guarde en el archivo "software_fj.log"
logger = SistemaLogger("software_fj.log")

# Creamos el gestor pasándole el logger, igual que en soluciontrabajocolaborativo.py
gestor = GestorSoftwareFJ(logger)

# Escribimos en el log que se abrió la interfaz gráfica
logger.registrar_evento("Se inició la interfaz gráfica de clientes.")


# ==============================================================================
# 2. FUNCIONES PARA QUE LOS BOTONES Y LA TABLA FUNCIONEN
# ==============================================================================

# ==============================================================================
# 3. CREACIÓN DE LA VENTANA PRINCIPAL (TKINTER)
# ==============================================================================
root = tk.Tk()
root.title("Gestión de Clientes - Software FJ")

# Panel izquierdo (Tools frame) donde va el formulario
tools_frame = tk.Frame(root, width=320, height=600, bg="skyblue")
tools_frame.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)
tools_frame.pack_propagate(False)  # Mantiene el ancho definido en tools_frame

tk.Label(
    tools_frame,
    text="Menu",
    bg="skyblue",
).pack(padx=5, pady=5)

# Creamos las pestañas (Notebook)
notebook = ttk.Notebook(tools_frame)
notebook.pack(expand=True, fill="both", padx=5, pady=5)

# Contenedor para la pestaña "Clientes" dentro del Notebook
tab_tools = tk.Frame(notebook)
notebook.add(tab_tools, text="Registrar Cliente")

# Campo para identificar al cliente
label_id = tk.Label(tab_tools, text="ID del cliente (ej: CLI-01):")
label_id.pack(pady=(10, 0))
entrada_id = tk.Entry(tab_tools, width=30)
entrada_id.pack(pady=5)

# Campo para el nombre del cliente
label_nombre = tk.Label(tab_tools, text="Nombre completo:")
label_nombre.pack()
entrada_nombre = tk.Entry(tab_tools, width=30)
entrada_nombre.pack(pady=5)

# Campo para el documento de identidad
label_documento = tk.Label(tab_tools, text="Documento de identidad:")
label_documento.pack()
entrada_documento = tk.Entry(tab_tools, width=30)
entrada_documento.pack(pady=5)

# Campo para el correo electrónico
label_email = tk.Label(tab_tools, text="Correo electrónico:")
label_email.pack()
entrada_email = tk.Entry(tab_tools, width=30)
entrada_email.pack(pady=5)

# Campo para el teléfono del cliente
label_telefono = tk.Label(tab_tools, text="Número de teléfono:")
label_telefono.pack()
entrada_telefono = tk.Entry(tab_tools, width=30)
entrada_telefono.pack(pady=5)

# Botón para registrar clientes: con command=... lo conectamos a nuestra función
boton_registrar = tk.Button(
    tab_tools,
    text="Registrar cliente",
    bg="green",
    fg="white",
    width=20,
    command=registrar_cliente_boton,
)
boton_registrar.pack(pady=15)


# ==============================================================================
# 4. CONTENEDOR DERECHO PARA LA TABLA DE CLIENTES
# ==============================================================================
panel_derecho = tk.Frame(root, width=320, height=400, bg="skyblue")
panel_derecho.pack(padx=5, pady=5, fill="both", expand=True)

tk.Label(
    panel_derecho,
    text="Clientes registrados",
    bg="grey",
    fg="white",
).pack(pady=(0, 5), fill=tk.X)

# Frame para agrupar la tabla y su barra de desplazamiento (scrollbar)
tabla_frame = tk.Frame(panel_derecho)
tabla_frame.pack(expand=True, fill=tk.BOTH)

columnas = ("id", "nombre", "documento", "email", "telefono")
tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)

# Configurar encabezados y ancho de columnas
encabezados = {
    "id": ("ID", 70),
    "nombre": ("Nombre completo", 160),
    "documento": ("Documento", 120),
    "email": ("Correo electrónico", 170),
    "telefono": ("Teléfono", 110),
}

for col, (texto, ancho) in encabezados.items():
    tabla.heading(col, text=texto)
    tabla.column(col, width=ancho, anchor=tk.W)

scrollbar = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=tabla.yview)
tabla.configure(yscrollcommand=scrollbar.set)

tabla.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# ==============================================================================
# 5. CONTENEDOR INFERIOR PARA MOSTRAR LOS LOGS EN PANTALLA
# ==============================================================================
logs_frame = tk.Frame(root, width=320, height=160, bg="red")
logs_frame.pack(padx=5, pady=5, fill="both")
logs_frame.pack_propagate(False)  # Mantiene el alto definido en logs_frame

tk.Label(
    logs_frame,
    text="LOGS",
    bg="red",
    fg="white",
).pack(padx=5, pady=2)

# Cuadro de texto donde iremos mostrando los mensajes de éxito o error
texto_logs = tk.Text(logs_frame, height=6, state="disabled")
texto_logs.pack(padx=5, pady=5, expand=True, fill="both")

# Mensaje inicial para que el usuario vea que el sistema ya está listo
escribir_en_logs("[INFO] Sistema conectado y listo para registrar clientes.")

# Iniciamos el ciclo principal de la ventana para que se quede abierta
root.mainloop()
