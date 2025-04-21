import os
import json
import time
import datetime
import random
import pickle
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

COOKIES_PATH = "whatsapp_cookies.pkl"
LEADS_JSON_PATH = "leads.json"
TIEMPO_ENTRE_MENSAJES = 15

fecha_actual = datetime.datetime.now()


def obtener_driver_existente():
    try:
        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        print("Ventana existente detectada y reutilizada.")
        return driver
    except Exception:
        return None


def iniciar_navegador(headless=False):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=es")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    driver.get("https://web.whatsapp.com/")
    return driver


def cargar_cookies(driver):
    if os.path.exists(COOKIES_PATH):
        with open(COOKIES_PATH, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()


def guardar_cookies(driver):
    with open(COOKIES_PATH, "wb") as file:
        pickle.dump(driver.get_cookies(), file)


def verificar_sesion_activa(driver):
    try:
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[tabindex='-1']"))
        )
        return True
    except Exception:
        return False


def enviar_mensaje(driver, numero, mensaje):
    try:
        mensaje_codificado = urllib.parse.quote(mensaje)
        url = f"https://web.whatsapp.com/send?phone={numero}&text={mensaje_codificado}"
        driver.get(url)

        boton_enviar = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Enviar']"))
        )
        boton_enviar.click()

        print(f"Mensaje enviado a {numero}.")
        time.sleep(TIEMPO_ENTRE_MENSAJES + random.uniform(1, 3))
        return True  
    except Exception as e:
        print(f"Error al enviar mensaje a {numero}: {e}")
        return False 
    

def cargar_leads():
    """Carga los leads desde un archivo JSON y evita errores si está vacío o corrupto."""
    if os.path.exists(LEADS_JSON_PATH):
        try:
            with open(LEADS_JSON_PATH, "r", encoding="utf-8") as file:
                contenido = file.read().strip()
                if not contenido:
                    return []
                return json.loads(contenido)
        except json.JSONDecodeError:
            print("Error: El archivo leads.json está corrupto o mal formado.")
            return []
    return []


def actualizar_leads(nuevos_leads):
    """Actualiza leads sin sobrescribir, solo cambia flag_envio si el número ya existe."""
    leads_existentes = cargar_leads()
    leads_dict = {lead["id"]: lead for lead in leads_existentes}

    for nuevo_lead in nuevos_leads:
        numero = nuevo_lead["id"]
        if numero in leads_dict:
            
            if not leads_dict[numero]["flag_envio"] and nuevo_lead["flag_envio"]:
                leads_dict[numero]["flag_envio"] = True
        else:
            leads_dict[numero] = nuevo_lead  

    with open(LEADS_JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(list(leads_dict.values()), file, indent=4, ensure_ascii=False)


def procesar_envios():
    driver = obtener_driver_existente() or iniciar_navegador(headless=False)

    try:
        if not verificar_sesion_activa(driver):
            print("Cargando cookies o esperando inicio de sesión manual...")
            cargar_cookies(driver)
            if not verificar_sesion_activa(driver):
                print("Por favor, inicia sesión manualmente en WhatsApp Web.")
                WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div[tabindex='-1']")
                    )
                )
                guardar_cookies(driver)

        leads = cargar_leads()

        leads_actualizados = []

        for lead in leads:
            if not lead["flag_envio"]:
                exito = enviar_mensaje(driver, lead["numero"], lead["mensaje"])
                if exito:
                    lead["flag_envio"] = True
            leads_actualizados.append(lead)

        actualizar_leads(leads_actualizados)

        print("Proceso finalizado. La ventana de navegador permanece abierta.")
    except Exception as e:
        print(f"Error en el flujo principal: {e}")
    finally:
        print(
            "El programa ha terminado su ejecución. Puedes volver a ejecutarlo cuando sea necesario."
        )



def mensaje_bienvenida(nombre, contrato, afiliados):
    return (
        f"*Estimado(a) {nombre} ,*\n\n"
        "Ahora que ya te encuentras afiliado al Plan Salud Segura, es momento de disfrutar con tu familia con total tranquilidad.\n\n"

        f"Las detalles de su afiliación son:\n"
        f"Número de contrato: {contrato}\n "
        f"Total de afiliados: {afiliados}\n\n"

        f"*¿Conoces la cobertura de tu plan?* 🤔\n"
        "Salud Segura te ofrece beneficios según tu plan contratado, conócelos aquí: https://www.youtube.com/watch?v=uq76CcVu11Y\n\n"

        "Además, te informamos que contamos con la plataforma en línea Mi Salud Segura donde podrás pagar la cuota de tu plan desde donde te encuentres. 📲 Ingresa aquí: https://bit.ly/MiSaludSegura\n\n"
        "*Si no cuentas con tus credenciales solicítalos por este medio.\n"

        "En *Salud Segura*, estamos comprometidos con tu salud y bienestar.\n"
    )


if __name__ == "__main__":
    # leads_nuevos = [
    #     {
    #         "numero": "51959799067",
    #         "mensaje": mensaje_bienvenida(
    #             "Karin Miljanovich",
    #             "2025-0000001",
    #             2
    #         ),
    #         "flag_envio": False,
    #         "fecha_lead": "2025-04-08",
    #         "id": "51959799067" + str("2025-04-08").replace("-", ""),
    #     },
    # ]

    # actualizar_leads(leads_nuevos)
    # #procesar_envios()
    # # print(leads_nuevos)
    pass


