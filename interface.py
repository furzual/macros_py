import tkinter as tk
from tkinter import ttk

def set_body_req(mode):
    if mode == "test":
        body_req.set("test")
    elif mode == "fdmx":
        body_req.set("fdmx")
    elif mode == "fgb":
        body_req.set("fgb")

def open_file(file_name):
    # Redirecciona a los archivos correspondientes
    if file_name == "Carga":
        import carga_masiva
    elif file_name == "Consulta":
        import get_store2
    elif file_name == "Nodo":
        import new_node_assign
    elif file_name == "Eliminar":
        import delete_stores_test
    elif file_name == "Personalizado":
        import custom_req

# Crear la ventana principal
root = tk.Tk()
root.title("Carga Masivas")

# Variable para el modo (test, fdmx, fgb)
body_req = tk.StringVar()

# Crear una etiqueta para el modo
mode_label = tk.Label(root, text="Selecciona una opción:")
mode_label.grid(row=0, column=0, padx=30, pady=10, columnspan=20)



# Crear botones para cada opción en dos columnas
options = ["Carga", "Consulta", "Nodo", "Eliminar", "Personalizado"]
row_num = 2
col_num = 0
for option in options:
    button = tk.Button(root, text=option, command=lambda option=option: open_file(option))
    button.grid(row=row_num, column=col_num, padx=30, pady=10)
    col_num = (col_num + 1) % 2
    if col_num == 0:
        row_num += 1

# Ejecutar la aplicación
root.mainloop()
