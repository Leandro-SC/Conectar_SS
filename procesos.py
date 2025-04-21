import os
import pandas as pd
from datetime import datetime, timedelta, date
from dateutil.parser import parse
from dotenv import load_dotenv
from helpers import (
convertir_datetime_to_date,
limpiar_celular,
)
from bd import execute_stored_procedure

from mensajes import mensaje_bienvenida,procesar_envios


# Cargar las variables de entorno
load_dotenv()

anio_actual = datetime.now().year
mes_actual = datetime.now().month
dia_actual = datetime.now().day + 1
fecha_actual = f"{dia_actual}/{mes_actual}/{anio_actual}"
fecha_actual_fomato = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
fecha_actual_fomato_agenda = date.today().strftime("%Y-%m-%d")
fecha_actual_sin_formato =  (date.today() - timedelta(days=15)).strftime("%Y-%m-%d")

TD_SALUD_SEGURA = os.getenv("TD_SALUD_SEGURA")

# Ejecutar procedimiento almacenado y obtener DataFrame
df_tabla = execute_stored_procedure(TD_SALUD_SEGURA)


def convertir_tabla_afiliados():
    df_afiliados = df_tabla
    df_afiliados_nuevo = (
        df_afiliados.groupby(
            ["CONTRATANTE", "Contrato", "Tipo_Contrato", "email_aseg", "num_cel", "FECHA_DOCUMENTACION","DOCUMENTACION"]
        )
        .agg(afiliados_unicos=("cod_aseg", lambda x: x.nunique()))
        .reset_index()
    )


    df_afiliados_nuevo["num_cel"] = df_afiliados_nuevo["num_cel"].apply(limpiar_celular)
    df_afiliados_nuevo["FECHA_DOC_TEMP"] = df_afiliados_nuevo["FECHA_DOCUMENTACION"].apply(convertir_datetime_to_date)


    filtro_documentacion = (
         (df_afiliados_nuevo["FECHA_DOC_TEMP"] >= fecha_actual_sin_formato) &
         (df_afiliados_nuevo["DOCUMENTACION"] == "Entregado") 
    )

    df_filtrado = df_afiliados_nuevo[filtro_documentacion]

    df_afiliados_final = df_filtrado[
        [
            "CONTRATANTE",
            "Contrato",
            "Tipo_Contrato",
            "email_aseg",
            "num_cel",
            "FECHA_DOC_TEMP",
            "DOCUMENTACION",
            "afiliados_unicos",
        ]
    ]

    return df_afiliados_final



def convertir_mapa(data):
    datos_contactos = []
    for indice, fila in data.iterrows():
        paciente = {
            "nombre": fila["CONTRATANTE"],
            "whatsapp": "51" + fila["num_cel"],
            "email": fila["email_aseg"],
            "tipo_contrato": fila["Tipo_Contrato"],
            "nro_contrato": fila["Contrato"],
            "fecha_registro":fila["FECHA_DOC_TEMP"],
            "total_afiliados":fila["afiliados_unicos"],
            "flag_envio": False,
        }
        datos_contactos.append(paciente)

    return datos_contactos



def convertir_mapa_brevo(data):
    datos_contactos = []
    lead = {}
    for indice, fila in data.iterrows():
        lead = {
            "nombre": fila["CONTRATANTE"],
            "whatsapp": "51" + fila["num_cel"],
            "email": fila["email_aseg"],
            "tipo_contrato": fila["Tipo_Contrato"],
            "nro_contrato": fila["Contrato"],
            "fecha_registro":fila["FECHA_DOC_TEMP"],
            "total_afiliados":fila["afiliados_unicos"],
            "flag_envio": False,
        }

        datos_contactos.append(lead)

        
    return datos_contactos


def convertir_formato_whatsapp(data_pacientes):
    lista_final = []
    for i in data_pacientes:
        lista_final.append({
            "nombre": i["nombre"],
            "whatsapp": i["whatsapp"],
            "tipo_contrato": i["tipo_contrato"],
            "nro_contrato": i["nro_contrato"],
            "fecha_actualizacion":i["fecha_registro"],
            "total_afiliados":i["total_afiliados"],
            "flag_envio": False,
        })

    return lista_final

def exportar_mapa():
    df_afiliados = convertir_tabla_afiliados()
    datos = convertir_mapa_brevo(df_afiliados)

    return datos



def envio_agenda():

    df_afiliados = convertir_tabla_afiliados()
    datos = convertir_mapa(df_afiliados)
    return convertir_formato_whatsapp(datos)


def simulador_envio_mensajes():
    # Utilizar los datos obtenidos en envío de agenda
    datos = envio_agenda()
    lista_mensaje = []
    for i in datos:
        lista_mensaje.append({
            "numero": i["whatsapp"],
            "mensaje": mensaje_bienvenida(i["nombre"], i["nro_contrato"], i["total_afiliados"]),
            "flag_envio": i["flag_envio"],
            "id": i["whatsapp"] + str(i["fecha_actualizacion"]).replace("-", ""),
        })
    return procesar_envios()



if __name__ == "__main__":
    datos_afiliados = convertir_tabla_afiliados()
    print(datos_afiliados)
    #print(convertir_mapa(datos_afiliados))
    #print(fecha_actual_sin_formato)
    #print(simulador_envio_mensajes())
    #print(exportar_mapa())
    pass











