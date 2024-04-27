import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from Funciones_gpt import descripcion_GPT
import pandas as pd
from openai import OpenAI
import threading






def mostrar_descripcion(event=None):
    producto_seleccionado = combo_productos.get()
    if producto_seleccionado in productos_descripciones:
        descripcion = productos_descripciones[producto_seleccionado]
        entry_descripcion.delete(1.0, tk.END)
        entry_descripcion.insert(tk.END, descripcion)
    else:
        messagebox.showwarning("Advertencia", "Seleccione un producto válido")

def generar_desc():
    def generar_desc_thread():
        
        # Mostrar indicador de carga
        boton_ejecutar.config(text="Generando...", state=tk.DISABLED)

        df = pd.read_csv('datos_productos.csv')

        for index, row in df.iterrows():
            nombre_producto = row['Producto']
            
            descripcion_generada = descripcion_GPT(nombre_producto)
            
            df.loc[df['Producto'] == nombre_producto, 'Descripcion'] = descripcion_generada

        df.to_csv('datos_productos.csv', index=False)
        
        boton_ejecutar.config(text="Generar Descripciones", state=tk.NORMAL)

        actualizar_combo_box()

    threading.Thread(target=generar_desc_thread).start()

def actualizar_combo_box():
    global productos_descripciones
    df_actualizado = pd.read_csv('datos_productos.csv')
    productos_descripciones = df_actualizado.set_index('Producto').to_dict()['Descripcion']
    combo_productos['values'] = list(productos_descripciones.keys())

try:
    df = pd.read_csv('datos_productos.csv')
    productos_descripciones = df.set_index('Producto').to_dict()['Descripcion']
except FileNotFoundError:
    messagebox.showerror("Error", "El archivo de datos no se encontró.")

root = tk.Tk()
root.title("Generador de Descripciones de Productos")

combo_productos = ttk.Combobox(root, values=list(productos_descripciones.keys()), width=30)
combo_productos.grid(row=0, column=0, padx=10, pady=10)
combo_productos.bind("<<ComboboxSelected>>", mostrar_descripcion)

entry_descripcion = tk.Text(root, wrap=tk.WORD, width=50, height=10)
entry_descripcion.grid(row=0, column=1, padx=10, pady=10)

boton_ejecutar = tk.Button(root, text="Generar Descripciones", command=generar_desc)
boton_ejecutar.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
