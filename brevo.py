import os
import requests
import certifi
from requests.exceptions import SSLError, HTTPError, RequestException
from dotenv import load_dotenv

load_dotenv()

# Configuración de la API
API_KEY = str(os.getenv("KEY_BREVO"))
BASE_URL = "https://api.brevo.com/v3"


def enviar_contactos(contactos, lista_id=None):
    url = f"{BASE_URL}/contacts"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    data = {
        "email": None,
        "attributes": {},
        "listIds": [lista_id] if lista_id else [],
        "updateEnabled": True,
    }

    for contacto in contactos:
        data["email"] = contacto.get("email")
        data["attributes"] = {k: v for k, v in contacto.items() if k != "email"}

        try:
            response = requests.post(
                url, json=data, headers=headers, verify=certifi.where()
            )
            response.raise_for_status()

            if response.status_code == 204:
                print(
                    f"Contacto enviado exitosamente (sin contenido): {contacto.get('email')}"
                )
            else:
                print(f"Contacto enviado exitosamente: {contacto.get('email')}")
                print(response.json())

        except SSLError as e:
            print(f"Error SSL al enviar el contacto {contacto.get('email')}: {e}")
        except HTTPError as e:
            print(f"Error HTTP al enviar el contacto {contacto.get('email')}: {e}")
        except RequestException as e:
            print(f"Error en la solicitud para {contacto.get('email')}: {e}")
        except ValueError:
            print("La respuesta no contiene JSON válido.")
            print(f"Contenido: {response.text}")


def actualizar_lista_contactos(lista_id, contactos):
    url = f"{BASE_URL}/contacts/import"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    data = {"listIds": [lista_id], "jsonBody": contactos, "updateEnabled": True}

    try:
        response = requests.post(
            url, json=data, headers=headers, verify=certifi.where()
        )
        response.raise_for_status()
        print(f"Lista de contactos actualizada exitosamente (ID: {lista_id}).")
        print(response.json())

    except RequestException as e:
        print("Error al actualizar lista de contactos.")
        print(f"Detalle: {e}")


def consultar_estado_proceso(process_id):
    url = f"{BASE_URL}/processes/{process_id}"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    try:
        response = requests.get(url, headers=headers, verify=certifi.where())
        response.raise_for_status()
        estado = response.json()
        print(f"Estado del proceso ({process_id}): {estado['status']}")
        print(f"Detalles: {estado}")

    except RequestException as e:
        print("Error al consultar el estado del proceso.")
        print(f"Detalle: {e}")


if __name__ == "__main__":
    # Lista de contactos
    contactos = [
        {
            "email": "contacto7@example.com",
            "attributes": {
                "NOMBRE": "Camilo Sesti",
                "WHATSAPP": "904904904",
                "TIPO_CONTRATO": "Tipo A",
                "NRO_CONTRATO": "123456",
                "FECHA_REGISTRO": "2023-10-01",
                "TOTAL_AFILIADOS": 5,
            },
        },
        {
            "email": "contacto8@example.com",
            "attributes": {
                "NOMBRE": "Julia Esther",
                "WHATSAPP": "904904905",
                "TIPO_CONTRATO": "Tipo B",
                "NRO_CONTRATO": "123455",
                "FECHA_REGISTRO": "2023-10-01",
                "TOTAL_AFILIADOS": 1,
            },
        },
        {
            "email": "contacto9@example.com",
            "attributes": {
                "NOMBRE": "Fresialinda Casinelli",
                "WHATSAPP": "904904906",
                "TIPO_CONTRATO": "Tipo A",
                "NRO_CONTRATO": "123457",
                "FECHA_REGISTRO": "2023-10-01",
                "TOTAL_AFILIADOS": 2,
            },
        },
    ]

    LISTA_ID = 145  # Reemplazar con el ID real de tu lista en Brevo
    # enviar_contactos(contactos, LISTA_ID)
    # actualizar_lista_contactos(LISTA_ID, contactos)

