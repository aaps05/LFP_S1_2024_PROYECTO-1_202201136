import tkinter as tk
from tkinter import filedialog, messagebox
from Analizador import instruccion_inicio
import ast
ventana = tk.Tk()
ventana.title("Proyecto 1 Lenguajes Formales y de Programación")

def abrir_archivo():
    file_name = filedialog.askopenfilename(filetypes=[("Archivos LFP", "*.lfp")])
    if file_name:
        with open(file_name, 'r', encoding="utf-8") as file:
            contenido = file.read()
            print(contenido)
            txt_entrada.delete(1.0, tk.END)
            txt_entrada.insert(tk.END, contenido)

            lexemas, errores = instruccion_inicio(contenido)  # Separar tokens y errores
            mostrar_lexemas(lexemas)
            mostrar_errores(errores)
            print("LEXEMAS DESPUÉS DE ABRIR ARCHIVO")
            print(lexemas)
            print("ERRORES DESPUÉS DE ABRIR ARCHIVO")
            print(errores)

            txt_entrada.delete(1.0, tk.END)
            txt_entrada.insert(tk.END, contenido)
            txt_salida.delete(1.0, tk.END)



def mostrar_lexemas(lexemas):
    lexemas_filtrados = []  # Lista para almacenar los lexemas deseados
    for token in lexemas:
        if token['tkn'] != 'TOKEN_NO_DESEADO':  # Reemplaza 'TOKEN_NO_DESEADO' con el tipo de token que deseas mantener
            lexemas_filtrados.append(token)  # Agrega el token deseado a la lista filtrada
    for token in lexemas_filtrados:
        tkn = token['tkn']
        lxm = token['lxm']
        linea = token['fila']
        columna = token['columna']
        print(f'Token: {tkn}, Lexema: {lxm}, Linea: {linea}, Columna: {columna}')

def mostrar_errores(errores):
    for error in errores:
        #txt_errores.insert(tk.END, f'Tipo: {error["tipo"]}, Descripción: {error["descripcion"]}, Fila: {error["fila"]}, Columna: {error["columna"]}\n')
        print(f'Tipo: {error["tipo"]}, Descripción: {error["descripcion"]}, Fila: {error["fila"]}\n')


def guardar_archivo():
    file_name = filedialog.asksaveasfilename(defaultextension=".lfp", filetypes=[("Archivos LFP", "*.lfp")])
    if file_name:
        contenido = txt_entrada.get(1.0, tk.END)
        with open(file_name, 'w', encoding="utf-8") as file:
            file.write(contenido)
            print(contenido)
        messagebox.showinfo("Guardar","Archivo guardado correctamente.")

def generar_html(tokens_info, errores_info):
    with open('Reportes.html', 'w') as f:
        # Escribir el encabezado del HTML
        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<title>Tokens y Errores</title>\n')
        #f.write('<style>th, td {border: "2px solid black"; border-radius: "5px"}</style>\n')
        f.write('</head>\n')
        f.write('<body>\n')

        # Escribir la tabla de tokens
        f.write('<h2>Tokens</h2>\n')
        f.write('<table border="2">\n')
        f.write('<tr><th style="background-color: lavender">Token</th><th style="background-color: lavender">Lexema</th><th style="background-color: lavender">Fila</th><th style="background-color: lavender">Columna</th></tr>\n')
        for token_info in tokens_info:
            f.write('<tr>')
            f.write(f'<td>{token_info["tkn"]}</td>')
            f.write(f'<td>{token_info["lxm"]}</td>')
            f.write(f'<td>{token_info["fila"]}</td>')
            f.write(f'<td>{token_info["columna"]}</td>')
            f.write('</tr>\n')
        f.write('</table>\n')

        # Escribir la tabla de errores
        f.write('<h2>Errores</h2>\n')
        f.write('<table border="1">\n')
        f.write('<tr><th style="background-color: lavender">Tipo</th><th style="background-color: lavender">Descripción</th><th style="background-color: lavender">Fila</th><th style="background-color: lavender">Columna</th></tr>\n')
        for error_info in errores_info:
            f.write('<tr>')
            f.write(f'<td>{error_info["tipo"]}</td>')
            f.write(f'<td>{error_info["descripcion"]}</td>')
            f.write(f'<td>{error_info["fila"]}</td>')
            f.write(f'<td>{error_info["columna"]}</td>')
            f.write('</tr>\n')
        f.write('</table>\n')

        # Cerrar el HTML
        f.write('</body>\n')
        f.write('</html>\n')


def traducir(errores):
    contenido = txt_entrada.get(1.0, tk.END)
    lexemas, errores = instruccion_inicio(contenido)  # Separar tokens y errores
    print("LEXEMAS ANTES DE TRADUCIR")
    print(lexemas)
    print("")
    print("ERRORES ANTES DE TRADUCIR")
    print(errores)
    print("")
    
    # Generar HTML para los tokens y errores
    generar_html(lexemas, errores)

    # Mostrar los errores léxicos en un cuadro de diálogo
    if errores:
        messagebox.showerror("Errores léxicos", "\n".join([f"{error['tipo']}: {error['descripcion']} (Fila: {error['fila']}, Columna: {error['columna']})" for error in errores]))
    
    # Mostrar la traducción del contenido y las tablas HTML en el área de texto de salida
    txt_salida.delete(1.0, tk.END)



lista_errores = []

frame_ventana=tk.Frame(ventana)
ventana.geometry("760x560")
frame_ventana.place(x=120, y=100)

#Botón para abrir archivo
boton_abrir_archivo=tk.Button(ventana, text="Subir archivo", command=abrir_archivo)
boton_abrir_archivo.place(x=50, y=50, width=100, height=30)

#Botón para guardar archivo
boton_abrir_archivo=tk.Button(ventana, text="Guardar cambios", command=guardar_archivo)
boton_abrir_archivo.place(x=50, y=480, width=100, height=30)

#Botón para traducir
boton_traducir_archivo=tk.Button(ventana, text="Traducir", command=lambda: traducir(lista_errores))
boton_traducir_archivo.place(x=250, y=480, width=100, height=30)

label_1=tk.Label(frame_ventana, text="Texto de entrada")
label_1.grid(row=0, column=0)
#label_1.place(x=50, y=50, width=100, height=30)
txt_entrada=tk.Text(frame_ventana, width=30, height=20)
txt_entrada.grid(row=1, column=0, padx=0, pady=0)

label_2=tk.Label(frame_ventana, text="HTML generado")
label_2.grid(row=0, column=2)
#label_1.place(x=50, y=50, width=100, height=30)
txt_salida=tk.Text(frame_ventana, width=30, height=20)
txt_salida.grid(row=1, column=2, padx=30, pady=0)

ventana.mainloop() 