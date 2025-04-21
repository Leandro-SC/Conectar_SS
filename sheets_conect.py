import os
import sys
import pandas as pd
import gspread
from datetime import datetime, timedelta, date
from dateutil.parser import parse
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

from dotenv import load_dotenv

load_dotenv()

def resource_path(relative_path):
    """ Retorna la ruta correcta del archivo en PyInstaller o modo normal """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)


client_secrets_path = resource_path('client_secrets.json')

credenciales = ServiceAccountCredentials.from_json_keyfile_name(client_secrets_path, scope)
cliente = gspread.authorize(credenciales)

sheets_key = str(os.getenv("KEY_SHEET_LEADS_SJT"))


def conectar_google_sheets():
    libro = cliente.open_by_key(sheets_key)
    hoja = libro.worksheet("Afiliados")
    return hoja

def obtener_datos_existentes():
    hoja = conectar_google_sheets()
    datos = hoja.get_all_values()
    if datos:
        return pd.DataFrame(datos[1:], columns=datos[0])  
    return pd.DataFrame()

def insertar_datos(diccionario_datos):

    hoja = conectar_google_sheets()
    datos = obtener_datos_existentes().to_numpy().tolist()
    ultima_fila = len(hoja.get_all_values())
    datos_a_insertar = []
    duplicados = []    
    
    if not isinstance(diccionario_datos, list) or not diccionario_datos:
        print("Los datos proporcionados no son válidos o están vacíos.")
        return

    for registro in diccionario_datos:
        correo = registro.get("email", "")
        celular = registro.get("whatsapp", "")
        flag_correo = True
        flag_whatsapp = True
        fecha_envio = (date.today()).strftime("%Y-%m-%d")

        if any(correo in fila and celular in fila for fila in datos):
            duplicados.append(registro)
        else:
            datos_a_insertar.append([
                registro.get("nombre", ""),
                correo,
                celular,
                registro.get("tipo_contrato", ""),
                registro.get("nro_contrato",""),
                registro.get("fecha_registro", ""),
                registro.get("total_afiliados", ""),
                flag_correo,
                flag_whatsapp,
                fecha_envio,
            ])

    if duplicados:
        
        print("Registros duplicados encontrados:")
        for d in duplicados:
            print(f"Correo: {d.get('Correo_Electronico', '')}, Celular: {d.get('Celular', '')}")

    if datos_a_insertar:
        rango_inicio = f"A{ultima_fila + 1}"
        hoja.update(rango_inicio, datos_a_insertar)
        print(f"Se insertaron {len(datos_a_insertar)} registros en la hoja.")
    else:
        print("No se insertaron registros nuevos, todos los datos eran duplicados.")



if __name__ == "__main__":
    prueba = [
        {
            "nombre": "Camilo Solvidar",
            "email": "prueba@correo.com",
            "whatsapp": "904904904",
            "tipo_contrato": "Tipo A",
            "nro_contrato": "123456",
            "fecha_registro": "2025-01-25",
            "total_afiliados": "5"


        },
        {
          "nombre": "Ana Sauñe",
            "email": "prueba2@correo.com",
            "whatsapp": "904904905",
            "tipo_contrato": "Tipo B",
            "nro_contrato": "123457",
            "fecha_registro": "2025-01-24",
            "total_afiliados": "2"
        }
    ]


if __name__ == "__main__":
    #insertar_datos(prueba)
    # print(client_secrets_path)
    pass




