import re
from Abstract.Lexema import *
from Abstract.Abstract import *

reservadas = {
    'RINICIO': 'Inicio',
    'RENCABEZADO': 'Encabezado',
    'RTITULOPAGINA': 'TituloPagina',
    'RCUERPO': 'Cuerpo',
    'RTITULO': 'Titulo',
    'RFONDO': 'Fondo',
    'RPARRAFO': 'Parrafo',
    'RTEXTO': 'Texto',    
    'RCODIGO': 'Codigo',
    'RNEGRITA': 'Negrita',
    'RSUBRAYADO': 'Subrayado',
    'RTACHADO': 'Tachado',
    'RCURSIVA': 'Cursiva',
    'RSALTO': 'Salto',
    'RTABLA': 'Tabla',
    'RFILAS': 'filas',
    'RCOLUMNAS': 'columnas',
    'RELEMENTO': 'elemento',
    'RFILA': 'fila',
    'RCOLUMNA': 'columna',
    'RCANTIDAD': 'cantidad',
    'RTEXTOMINUSCULA': 'texto',
    'RPOSICION': 'posicion',
    'RFUENTE': 'fuente',
    'RCOLOR': 'color',
    'RTAMANO': 'tamaño',
    'LLAVEINICIO': '{',
    'LLAVEFINAL': '}',
    'CORCHETEINICIO': '[',
    'CORCHETEFINAL': ']',
    'DOSPUNTOS': ':',
    'COMA': ',',
    'PUNTOYCOMA': ';',
    'COMILLAINICIO': '"',
    'COMILLAFINAL': '"',
    'IGUAL': '=',
    'RCOMENTARIO': 'Comentario',
}


class Lexema:
    def __init__(self, token, lexema, linea, columna):
        self.token = token
        self.lexema = lexema
        self.linea = linea
        self.columna = columna


lexemas = list(reservadas.values())
global no_linea
global no_columna
global lista_lexemas
global instrucciones
global lista_errores

no_linea = 1
no_columna = 1
lista_lexemas = []
instrucciones = []
lista_errores = []


def instruccion_inicio(contenido):
    tokens = []
    errores = []
    lexema = ''
    reservadas_lexema = False
    no_linea = 1
    no_columna = 1

    # Expresión regular para buscar caracteres no válidos
    patron_caracteres_invalidos = r'[^A-Za-z0-9áéíóúüÁÉÍÓÚÜñÑ."{}\[\]:=,;\s]'

    # Buscar caracteres no válidos en el contenido
    matches = re.finditer(patron_caracteres_invalidos, contenido)
    for match in matches:
        errores.append({'tipo': 'Error léxico', 'descripcion': f'Carácter no válido: {match.group()}', 'fila': obtener_numero_linea(contenido, match.start()), 'columna': obtener_numero_columna(contenido, match.start())})

    for char in contenido:
        if char == '\n':
            no_linea += 1
            no_columna = 1
        elif char == '\"':
            reservadas_lexema = not reservadas_lexema
            if lexema and not reservadas_lexema:
                # Agregar el lexema como una cadena de texto
                tokens.append({'tkn': 'CADENADETEXTO', 'lxm': lexema.strip(), 'fila': no_linea, 'columna': no_columna})
                lexema = ''
        elif char in [':', '=', ';', ',']:
            # Agregar el lexema anterior si existe
            if lexema:
                tokens.append({'tkn': determinar_token(lexema), 'lxm': lexema.strip(), 'fila': no_linea, 'columna': no_columna})
                lexema = ''
            # Agregar el delimitador como un token separado
            if char == ':':
                tokens.append({'tkn': 'DOSPUNTOS', 'lxm': char, 'fila': no_linea, 'columna': no_columna})
            if char == '=':
                tokens.append({'tkn': 'IGUAL', 'lxm': char, 'fila': no_linea, 'columna': no_columna})
            elif char == ';':
                tokens.append({'tkn': 'PUNTOYCOMA', 'lxm': char, 'fila': no_linea, 'columna': no_columna})
            else:  # char == ','
                tokens.append({'tkn': 'COMA', 'lxm': char, 'fila': no_linea, 'columna': no_columna})
        elif char in ['{', '}']:
            # Agregar el lexema anterior si existe
            if lexema:
                tokens.append({'tkn': determinar_token(lexema), 'lxm': lexema.strip(), 'fila': no_linea, 'columna': no_columna})
                lexema = ''
            # Agregar la llave como un token separado
            if char == '{':
                tokens.append({'tkn': 'LLAVEINICIO', 'lxm': char, 'fila': no_linea, 'columna': no_columna})
            else:  # char == '}'
                tokens.append({'tkn': 'LLAVEFINAL', 'lxm': char, 'fila': no_linea, 'columna': no_columna})

        elif char in ['[', ']']:
            # Agregar el lexema anterior si existe
            if lexema:
                tokens.append({'tkn': determinar_token(lexema), 'lxm': lexema.strip(), 'fila': no_linea, 'columna': no_columna})
                lexema = ''
            # Agregar los corchete como un token separado
            if char == '[':
                tokens.append({'tkn': 'CORCHETEINICIO', 'lxm': char, 'fila': no_linea, 'columna': no_columna})
            else:  # char == ']'
                tokens.append({'tkn': 'CORCHETEFINAL', 'lxm': char, 'fila': no_linea, 'columna': no_columna})
            
        elif not char.isspace():
            lexema += char
        no_columna += 1

    # Manejar el último lexema
    if lexema and not reservadas_lexema:
        if lexema.upper() in reservadas:
            tokens.append({'tkn': 'PALABRA RESERVADA', 'lxm': lexema.strip(), 'fila': no_linea, 'columna': no_columna})
        else:
            tokens.append({'tkn': 'ID', 'lxm': lexema.strip(), 'fila': no_linea, 'columna': no_columna})


    return tokens, errores

# Funciones para obtener el número de línea y columna
def obtener_numero_linea(contenido, indice):
    return contenido.count('\n', 0, indice) + 1

def obtener_numero_columna(contenido, indice):
    ultima_linea_salto = contenido.rfind('\n', 0, indice)
    if ultima_linea_salto == -1:
        return indice + 1
    else:
        return indice - ultima_linea_salto

def crear_lexema(cadena):

    global no_linea
    global no_columna
    global lista_lexemas
    lexema = ''
    puntero = ''

    for char in cadena:
        puntero += char
        if char == ':' or char == '\"' or char == '=':
            if lexema in reservadas:
                return reservadas[lexema], cadena[len(puntero):].strip()  # Si el lexema es una palabra reservada, devolvemos su token correspondiente
            else:
                return lexema, cadena[len(puntero):].strip()  # Si no, devolvemos el lexema como está
        elif char == '\n' or char == '\r' or char == '{' or char == '}' or char == ',' or char == ';':
            return lexema, cadena.strip()  # Si encuentra un carácter especial que indica el final del token, devuelve el lexema
        else:
            lexema += char  # Agregamos el carácter al lexema

    return None, None

def determinar_token(lexema):
    # Determinar el token según el lexema
    if lexema in reservadas:
        return reservadas[lexema]
    elif lexema.startswith('"') and lexema.endswith('"'):
        return 'CADENADETEXTO'
    elif lexema.isdigit():
        return 'RNUMERO'
    elif lexema.isalpha():
        return lexema.upper()
    else:
        # Registrar el error
        lista_errores.append({'tipo': 'Error léxico', 'descripcion': f'Lexema no reconocido: {lexema}', 'fila': no_linea, 'columna': no_columna})
        return 'ERROR'
