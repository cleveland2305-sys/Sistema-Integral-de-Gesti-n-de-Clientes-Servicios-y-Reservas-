
import tkinter as tk
from tkinter import messagebox

# Ventana principal de gestión de clientes
ventana = tk.Tk()
ventana.title("Software FJ - Gestión de Clientes")
ventana.geometry("700x500")


# Título de la interfaz
titulo = tk.Label(ventana,text="REGISTRO DE CLIENTES",font=("Arial", 18, "bold"))
titulo.pack(pady=20)

# Campo para identificar al cliente
label_id = tk.Label(ventana, text="ID del cliente:")
label_id.pack()

entrada_id = tk.Entry(ventana, width=40)
entrada_id.pack(pady=5)


# Campo para el nombre del cliente
label_nombre = tk.Label(ventana, text="Nombre completo:")
label_nombre.pack()

entrada_nombre = tk.Entry(ventana, width=40)
entrada_nombre.pack(pady=5)

# Campo para el documento de identidad
label_documento = tk.Label(ventana, text="Documento de identidad:")
label_documento.pack()

entrada_documento = tk.Entry(ventana, width=40)
entrada_documento.pack(pady=5)


# Campo para el correo electrónico
label_email = tk.Label(ventana, text="Correo electrónico:")
label_email.pack()

entrada_email = tk.Entry(ventana, width=40)
entrada_email.pack(pady=5)


# Campo para el teléfono del cliente
label_telefono = tk.Label(ventana, text="Número de teléfono:")
label_telefono.pack()

entrada_telefono = tk.Entry(ventana, width=40)
entrada_telefono.pack(pady=5)


# Botón para registrar clientes
boton_registrar = tk.Button(ventana, text="Registrar cliente", bg="green", fg="white", width=20)

boton_registrar.pack(pady=15)

# Mantener abierta la ventana
ventana.mainloop()



