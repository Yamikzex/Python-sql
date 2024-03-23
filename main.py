import tkinter as tk
from tkinter import filedialog
import tabula
import pandas as pd
from sqlalchemy import create_engine

# Función para seleccionar un archivo PDF con Tkinter
def seleccionar_pdf():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir="C:/", title="Seleccionar archivo PDF", filetypes=[("PDF Files", "*.pdf")])
    return file_path

# Seleccionar el archivo PDF
archivo_pdf = seleccionar_pdf()

if not archivo_pdf:
    print("No se seleccionó ningún archivo PDF.")
else:
    try:
        # Leer el PDF
        tablas = tabula.read_pdf(archivo_pdf, pages='all', multiple_tables=True)

        # Crear el motor de SQLAlchemy
        engine = create_engine('mssql+pyodbc://DESKTOP-5NEKD7R\\SQLEXPRESS/pruebapractica?driver=SQL+Server+Native+Client+11.0&trusted_connection=yes')

        # Para cada tabla en el PDF
        for i, df in enumerate(tablas):
            # Convertir las cabeceras en una fila de datos
            headers = df.columns.tolist()
            df.columns = [f'Campo{j+1}' for j in range(len(df.columns))]  # Asegúrate de que estos nombres coinciden con los de tu tabla 'pdftable'
            df.loc[-1] = headers
            df.index = df.index + 1
            df.sort_index(inplace=True)

            # Escribir los datos en la base de datos
            df.to_sql('pdftable', con=engine, if_exists='append', index=False)

        print("Datos escritos en la base de datos exitosamente.")

    except Exception as e:
        print(f"Error durante el proceso: {e}")