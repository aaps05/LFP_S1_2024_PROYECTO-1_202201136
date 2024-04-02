import tkinter as tk
from tkinter import filedialog, messagebox
from Analizador import instruccion_inicio
import re

ventana = tk.Tk()
ventana.title("Proyecto 1 Lenguajes Formales y de Programación")

contenido_archivo = ""

def abrir_archivo():
    global contenido_archivo

    file_name = filedialog.askopenfilename(filetypes=[("Archivos LFP", "*.lfp")])
    if file_name:
        with open(file_name, 'r', encoding="utf-8") as file:
            contenido = file.read()
            print(contenido)
            txt_entrada.delete(1.0, tk.END)
            txt_entrada.insert(tk.END, contenido)

            lexemas, errores = instruccion_inicio(contenido)
            mostrar_lexemas(lexemas)
            mostrar_errores(errores)
            print("LEXEMAS DESPUÉS DE ABRIR ARCHIVO")
            print(lexemas)
            print("ERRORES DESPUÉS DE ABRIR ARCHIVO")
            print(errores)

            txt_entrada.delete(1.0, tk.END)
            txt_entrada.insert(tk.END, contenido)
            txt_salida.delete(1.0, tk.END)

#Función para extraer los datos del contenido del archivo .lfp
def extraer_datos_contenido(archivo_lfp):
    with open(archivo_lfp, 'r', encoding='utf-8') as f:
        contenido = f.read()

    datos_contenido = {}

    etiquetas = ["Titulo", "Fondo", "Parrafo", "Texto", "Codigo", "Negrita", "Subrayado", "Tachado", "Cursiva", "Salto", "Tabla"]

    for etiqueta in etiquetas:
        patron_etiqueta = re.compile('{}:\\s*{{(.*?)}}'.format(etiqueta), re.DOTALL)
        coincidencias = patron_etiqueta.findall(contenido)

        if coincidencias:
            datos_contenido[etiqueta] = []
            for match in coincidencias:
                datos = re.findall(r'(\w+)(?:=|:)(?:"([^"]*)"|(\w+))', match)
                datos_dict = {clave: valor.strip('"') for clave, valor, _ in datos}
                datos_contenido[etiqueta].append(datos_dict)

    return datos_contenido

#Extraer datos del contenido del archivo .lfp
datos_contenido = extraer_datos_contenido('archivoPrueba.lfp')

def generar_tabla(datos_tabla):
    tabla_html = '<table>\n'
    filas = int(datos_tabla["filas"])
    columnas = int(datos_tabla["columnas"])
    elementos = datos_tabla.get("elemento", {})

    for fila in range(1, filas + 1):
        tabla_html += '<tr>\n'
        for columna in range(1, columnas + 1):
            clave = f"fila{fila}columna{columna}"
            texto_elemento = elementos.get(clave, "")
            texto = re.search(r'"([^"]*)"$', texto_elemento).group(1) if texto_elemento else ""
            tabla_html += f'<td>{texto}</td>\n'
        tabla_html += '</tr>\n'

    tabla_html += '</table>\n'
    return tabla_html

def generar_html(datos):
    html = '<!DOCTYPE html>\n<html>\n<head>\n'
    
    #Procesar encabezado
    if "Encabezado" in datos:
        encabezado = datos["Encabezado"]
        if "TituloPagina" in encabezado:
            html += f'<title>{encabezado["TituloPagina"]}</title>\n'

    html += '</head>\n<body>\n'

    if "Titulo" in datos:
        titulo = datos["Titulo"][0]
        tamaño = titulo.get("tamaño", "")
        posicion = titulo.get("posicion", "izquierda")
        etiqueta = ""
        if tamaño == "t1":
            etiqueta = "h1"
        elif tamaño == "t2":
            etiqueta = "h2"
        elif tamaño == "t3":
            etiqueta = "h3"
        elif tamaño == "t4":
            etiqueta = "h4"
        elif tamaño == "t5":
            etiqueta = "h5"
        elif tamaño == "t6":
            etiqueta = "h6"
        
        posicion_css = "left" if posicion == "izquierda" else "right" if posicion == "derecha" else "center"
        fuente = titulo.get("fuente", "")
        color = titulo.get("color", "")
        #Traducción de colores a inglés
        color_ingles = {
            "rojo": "red",
            "azul": "blue",
            "verde": "green",
            "amarillo": "yellow",
            "negro": "black",
            "blanco": "white"
        }
        color_css = color_ingles.get(color, color)
        
        html += f'<{etiqueta} style="text-align: {posicion_css}; font-size: {tamaño}; color: {color_css}">{titulo["texto"]}</{etiqueta}>\n'

    if "Fondo" in datos:
        fondo = datos["Fondo"][0]
        color = fondo["color"]
        #Traducción de colores a inglés
        color_ingles = {
            "rojo": "red",
            "azul": "blue",
            "verde": "green",
            "amarillo": "yellow",
            "negro": "black",
            "blanco": "white"
        }
        color_css = color_ingles.get(color, color)
        html += f'<style>\n\tbody {{\n\t\tbackground-color: {color_css};\n\t}}\n</style>\n'

    if "Parrafo" in datos:
        parrafo = datos["Parrafo"][0]
        posicion = parrafo.get("posicion", "izquierda")
        posicion_css = "left" if posicion == "izquierda" else "right" if posicion == "derecha" else "center"
        html += f'<p style="text-align: {posicion_css}">{parrafo["texto"]}</p>\n'

    if "Texto" in datos:
        texto = datos["Texto"][0]
        posicion = texto.get("posicion", "izquierda")
        posicion_css = "left" if posicion == "izquierda" else "right" if posicion == "derecha" else "center"
        fuente = texto.get("fuente", "")
        color = texto.get("color", "")
        #Traducción de colores a inglés
        color_ingles = {
            "rojo": "red",
            "azul": "blue",
            "verde": "green",
            "amarillo": "yellow",
            "negro": "black",
            "blanco": "white"
        }
        color_css = color_ingles.get(color, color)
        tamaño = texto.get("tamaño", "")
        html += f'<span style="font-family: {fuente}; color: {color_css}; font-size: {tamaño}; text-align: {posicion_css}">{texto.get("texto", "")}</span>\n'

    if "Codigo" in datos:
        codigo = datos["Codigo"][0]
        posicion = codigo.get("posicion", "centro")
        posicion_css = "left" if posicion == "izquierda" else "right" if posicion == "derecha" else "center"
        html += f'<code style="text-align: {posicion_css}">{codigo["texto"]}</code>\n'

    if "Negrita" in datos:
        negrita = datos["Negrita"][0]
        html += f'<strong>{negrita["texto"]}</strong>\n'

    if "Subrayado" in datos:
        subrayado = datos["Subrayado"][0]
        html += f'<u>{subrayado["texto"]}</u>\n'

    if "Tachado" in datos:
        tachado = datos["Tachado"][0]
        html += f'<s>{tachado["texto"]}</s>\n'

    if "Cursiva" in datos:
        cursiva = datos["Cursiva"][0]
        html += f'<em>{cursiva["texto"]}</em>\n'

    if "Salto" in datos:
        salto = datos["Salto"][0]
        html += '<br>\n' * int(salto["cantidad"])

    if "Tabla" in datos:
        tabla = datos["Tabla"][0]
        html += generar_tabla(tabla)

    html += '</body>\n</html>'
    return html

#Generar HTML a partir de los datos extraídos del archivo .lfp
html_generado = generar_html(datos_contenido)

#Guardar el HTML generado en un archivo
with open('Archivo_HTML.html', 'w', encoding='utf-8') as f:
    f.write(html_generado)
print("")

#Función para mostrar los lexemas 
def mostrar_lexemas(lexemas):
    #Lista para almacenar los lexemas
    lexemas_filtrados = []  
    for token in lexemas:
        #Reemplaza 'TOKEN_NO_DESEADO' con el tipo de token que deseas mantener
        if token['tkn'] != 'TOKEN_NO_DESEADO':
            #Agrega el token deseado
            lexemas_filtrados.append(token)
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
        #Escribir el encabezado del HTML
        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<title>Tokens y Errores</title>\n')
        #f.write('<style>th, td {border: "2px solid black"; border-radius: "5px"}</style>\n')
        f.write('</head>\n')
        f.write('<body>\n')

        #Escribir la tabla de tokens
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

        #Escribir la tabla de errores
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

        #Cerrar el HTML
        f.write('</body>\n')
        f.write('</html>\n')


def traducir(errores):
    contenido = txt_entrada.get(1.0, tk.END)
    lexemas, errores = instruccion_inicio(contenido)  #Separar tokens y errores
    print("LEXEMAS ANTES DE TRADUCIR")
    print(lexemas)
    print("")
    print("ERRORES ANTES DE TRADUCIR")
    print(errores)
    print("")
    
    #Generar HTML para los tokens y errores
    generar_html(lexemas, errores)

    #Mostrar los errores léxicos en un cuadro de diálogo
    if errores:
        messagebox.showerror("Errores léxicos", "\n".join([f"{error['tipo']}: {error['descripcion']} (Fila: {error['fila']}, Columna: {error['columna']})" for error in errores]))
    
    #Mostrar la traducción del contenido y las tablas HTML en el área de texto de salida
    txt_salida.delete(1.0, tk.END)
    txt_salida.insert(tk.END, html_generado)
    print(datos_contenido)
    print("Se ha generado el archivo HTML correctamente.")



lista_errores = []

frame_ventana=tk.Frame(ventana)
ventana.geometry("870x560")
frame_ventana.place(x=120, y=100)

#Botón para abrir archivo
boton_abrir_archivo=tk.Button(ventana, text="Subir archivo", command=abrir_archivo)
boton_abrir_archivo.place(x=50, y=50, width=100, height=30)

#Botón para guardar archivo
boton_abrir_archivo=tk.Button(ventana, text="Guardar cambios", command=guardar_archivo)
boton_abrir_archivo.place(x=50, y=480, width=100, height=30)

#Botón para traducir
boton_traducir_archivo=tk.Button(ventana, text="Traducir", command=lambda: traducir(lista_errores))
boton_traducir_archivo.place(x=350, y=480, width=100, height=30)

label_1=tk.Label(frame_ventana, text="Texto de entrada")
label_1.grid(row=0, column=0)
#label_1.place(x=50, y=50, width=100, height=30)
txt_entrada=tk.Text(frame_ventana, width=40, height=20)
txt_entrada.grid(row=1, column=0, padx=0, pady=0)

label_2=tk.Label(frame_ventana, text="HTML generado")
label_2.grid(row=0, column=2)
#label_1.place(x=50, y=50, width=100, height=30)
txt_salida=tk.Text(frame_ventana, width=40, height=20)
txt_salida.grid(row=1, column=2, padx=30, pady=0)

ventana.mainloop() 