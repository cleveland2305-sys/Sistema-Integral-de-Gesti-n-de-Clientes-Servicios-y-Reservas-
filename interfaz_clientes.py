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
def escribir_en_logs(mensaje):
    """Esta función escribe un mensaje nuevo en el cuadro rojo de LOGS."""
    # Habilitamos el cuadro de texto para poder escribir en él
    texto_logs.config(state="normal")
    # Insertamos el mensaje al final con un salto de línea (\n)
    texto_logs.insert(tk.END, mensaje + "\n")
    # Hacemos scroll automático hacia abajo para ver siempre el último mensaje
    texto_logs.see(tk.END)
    # Volvemos a bloquear el cuadro de texto para que el usuario no lo borre por accidente
    texto_logs.config(state="disabled")
 
 
def actualizar_tabla():
    """Esta función borra la tabla y la vuelve a llenar con los clientes del gestor."""
    # Primero borramos todas las filas que ya estaban en la tabla para no repetirlas
    for fila in tabla.get_children():
        tabla.delete(fila)
 
    # Recorremos la lista de clientes que tiene guardada el gestor
    for cliente in gestor._clientes:
        # Insertamos cada cliente como una fila nueva en la tabla 
        tabla.insert(
            "",
            tk.END,
            values=(
                cliente.id,
                cliente.nombre,
                cliente.documento,
                cliente.email,
                cliente.telefono,
            ),
        )
 
 
def limpiar_campos():
    """Esta función borra lo que el usuario escribió en las cajitas de texto."""
    entrada_id.delete(0, tk.END)
    entrada_nombre.delete(0, tk.END)
    entrada_documento.delete(0, tk.END)
    entrada_email.delete(0, tk.END)
    entrada_telefono.delete(0, tk.END)
 
 
def registrar_cliente_boton():
    """Esta función se ejecuta cuando el usuario hace clic en 'Registrar cliente'."""
    # Sacamos el texto que escribió el usuario en cada cajita (Entry)
    id_cli = entrada_id.get()
    nombre = entrada_nombre.get()
    documento = entrada_documento.get()
    email = entrada_email.get()
    telefono = entrada_telefono.get()
 
    # Usamos try/except para atrapar los errores si el usuario escribe datos inválidos
    try:
        # Intentamos crear el objeto Cliente.
        # Aquí adentro la clase Cliente revisa que el nombre, documento, email y teléfono sean válidos.
        nuevo_cliente = Cliente(id_cli, nombre, documento, email, telefono)
 
        # Le pedimos al gestor que guarde al cliente en su lista
        se_guardo = gestor.registrar_cliente(nuevo_cliente)
 
        # Si el gestor devolvió True, significa que no estaba repetido y se guardó bien
        if se_guardo:
            # Actualizamos la tabla para que aparezca el cliente nuevo
            actualizar_tabla()
            # Escribimos en el cuadro de logs de la ventana
            escribir_en_logs(f"[OK] Se registró a {nuevo_cliente.nombre} (ID: {nuevo_cliente.id})")
            # Mostramos una ventanita avisando que todo salió bien
            messagebox.showinfo("Registro exitoso", "El cliente se registró correctamente.")
            # Limpiamos las cajitas para poder registrar otro cliente
            limpiar_campos()
        else:
            # Si devolvió False, es porque ya existía un cliente con ese ID o documento
            escribir_en_logs(f"[ERROR] Ya existe un cliente con ID '{id_cli}' o documento '{documento}'.")
            messagebox.showerror(
                "Cliente duplicado",
                "Ya existe un cliente registrado con ese ID o con ese documento.",
            )
 
    except SoftwareFJError as error:
        # Si faltó algún dato o el correo/teléfono/documento está mal, entramos aquí
        logger.registrar_error(error, "Error al registrar cliente desde la interfaz")
        escribir_en_logs(f"[ERROR] {error}")
        # Mostramos el mensaje de error exacto en una ventanita emergente
        messagebox.showerror("Dato inválido", str(error))

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
