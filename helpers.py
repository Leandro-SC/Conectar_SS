from datetime import datetime
from dateutil.parser import parse


#Meses en Mayúsculas
mes_mayusculas = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

def obtener_mes_mayusculas(mes):
    return mes_mayusculas.get(mes, "MES DESCONOCIDO")


def separar_mes_fecha(fecha):
    mes_texto_numero = fecha.split("/")[1]
    mes_numero = int(mes_texto_numero)

    return obtener_mes_mayusculas(mes_numero)

def convertir_fecha(fecha):
    dia, mes, anio = fecha.split("/")
    return f"{anio}-{mes}-{dia}"


def excluir_nombre(nombre):
    nombre = nombre.capitalize()
    #encontrar si existe una palabra en la cadena que contenga "NOMBRE"
    if "Hijo_1" in nombre:
        return " "
    else:
        return nombre

def convert_to_datetime(input_str, parserinfo=None):
    return parse(input_str, parserinfo=parserinfo)

def convert_to_text(texto):
    return str(texto)

def convertir_nombre_propio(nombre):
        if type(nombre) == str:
            return nombre.strip().title()
        else:
            return str(nombre).strip().title()

def convertir_a_12_horas(hora_24):
    hora_24 = hora_24.strip()
    return datetime.strptime(hora_24, "%H:%M").strftime("%I:%M %p").lstrip("0")  


def extraer_nombre(nombre_paciente):
    partes = nombre_paciente.split(",")
    nombre_extraido = ""
    nombre_extraido = " ".join(partes[-1:])
    if len(nombre_extraido.split()) > 1:
        partes_nombre = nombre_extraido.split(" ")
        solo_un_nombre = partes_nombre[:-1] 
        return solo_un_nombre[1].strip().capitalize()
    else:
        return nombre_extraido.strip().capitalize()




def convertir_fecha_letra(fecha):
    dia, mes, anio = fecha.split("/")
    mes_letra = obtener_mes_mayusculas(int(mes))
    return f"{dia} de {mes_letra} del {anio}"


def convertir_datetime_to_date(fecha_hora):
    fecha = fecha_hora.date()
    return fecha.strftime("%Y-%m-%d")

def limpiar_celular(celular):
    if isinstance(celular, str):
        celular = celular.replace(" ", "").replace("-", "").replace("+", "").replace("(", "").replace(")", "").strip()
    return celular


if __name__ =="__main__":
    #print(excluir_nombre(extraer_nombre("AGUILAR ALEGRE, HIJO_1 ")))
    #print(convertir_nombre_propio("un mensaje de prueba"))
    pass
    #convertir_datetime_to_date("2024-10-19 08:51:57.090")
    print("      51 999 999 999  ")
    print(limpiar_celular("      51 999 999 999  "))

