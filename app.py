import traceback

from dotenv import load_dotenv
from procesos import envio_agenda, convertir_mapa_brevo, convertir_tabla_afiliados, convertir_mapa
from mensajes import mensaje_bienvenida, procesar_envios, actualizar_leads
from brevo import enviar_contactos, actualizar_lista_contactos
from sheets_conect import insertar_datos

load_dotenv()

datos_whatsapp = envio_agenda()
datos_brevo = convertir_mapa_brevo(convertir_tabla_afiliados())
datos_formateados_landings = convertir_mapa(convertir_tabla_afiliados())


LISTA_ID = 145

def main():
    contactos_landing_brevo()
    envio_mensajes_whatsapp()
    #pass
 


def envio_mensajes_whatsapp():

    lista_mensaje = []

    for i in datos_whatsapp:
        lista_mensaje.append({
            "numero": "51"+i["whatsapp"],
            "mensaje": mensaje_bienvenida(i["nombre"], i["nro_contrato"], i["total_afiliados"]),
            "flag_envio": i["flag_envio"],
            "fecha_actualizacion": i["fecha_actualizacion"],
            "id": i["whatsapp"] + str(i["fecha_actualizacion"]).replace("-", ""),
        }) 

    actualizar_leads(lista_mensaje)
    
    return procesar_envios()


def contactos_landing_brevo():
    if datos_brevo:
        enviar_contactos(datos_brevo, LISTA_ID)
        actualizar_lista_contactos(LISTA_ID, datos_brevo)
        insertar_datos(datos_formateados_landings)
    else:
        print("No se encontraron leads para procesar.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error en el flujo principal: {e}")
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())






