from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import smtplib
import os
from selenium.webdriver.firefox.service import Service
import time
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText
from selenium.webdriver.firefox.options import Options
import asyncio
from telethon import TelegramClient

api_id = ''  # Reemplaza con tu API ID
api_hash = ''  # Reemplaza con tu API Hash
group_id = 0  # Reemplaza con el ID del grupo al que deseas enviar el mensaje
bot_token = ""

async def enviar_mensaje():
    api_id, api_hash, group_id, bot_token = leerVariablesTelegram()
    async with TelegramClient('session_name', api_id, api_hash) as client:
        await client.send_message(group_id, '¡HAY TURNOS! WEB:  https://www.exteriores.gob.es/Consulados/rosario/es/Comunicacion/Noticias/Paginas/Articulos/Instrucciones-para-solicitar-cita-previa.aspx')

#Este método lee las credenciales de correo de un txt en la ruta PADRE de este script.
def leerCredencialesDeCorreo():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    directorio_padre = os.path.abspath(os.path.join(directorio_actual, os.pardir))
    archivoCredenciales = os.path.join(directorio_padre, "credencialesCorreo.txt")
    with open(archivoCredenciales, "r") as file:
        lines = file.readlines()
        sender_email = lines[0].strip()
        sender_password = lines[1].strip()
    return sender_email, sender_password

def leerCorreoParaEnviar():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    directorio_padre = os.path.abspath(os.path.join(directorio_actual, os.pardir))
    archivoCredenciales = os.path.join(directorio_padre, "correosParaEnviar.txt")
    with open(archivoCredenciales, "r") as file:
        lines = file.readlines()
        receiver_emails = [line.strip() for line in lines]
    return receiver_emails

def leerVariablesTelegram():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    directorio_padre = os.path.abspath(os.path.join(directorio_actual, os.pardir))
    archivoVariables = os.path.join(directorio_padre, "telegram_bot.txt")
    with open(archivoVariables, "r") as file:
        lines = file.readlines()
        api_id = lines[0].strip()
        api_hash = lines[1].strip()
        group_id = int(lines[2].strip())
        bot_token = lines[3].strip()
    return api_id, api_hash, group_id, bot_token

#Este método envía un correo electrónico a los usuarios indicados en "recipient_email" usando SMTP.
def send_email():
    sender_email, sender_password = leerCredencialesDeCorreo()
    recipient_email = leerCorreoParaEnviar()
    subject = "HAY TURNOS!"
    body = "https://www.exteriores.gob.es/Consulados/rosario/es/Comunicacion/Noticias/Paginas/Articulos/Instrucciones-para-solicitar-cita-previa.aspx"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_email)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())

#Este método chequea si hay turnos, y si hay, envía un mail, sino no.
async def script_turno():
    #Aquí va el path de geckodriver
    gecko_driver_path = r"C:\firefox_webdriver\geckodriver.exe"
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(service=Service(executable_path=gecko_driver_path), options=options)
    #Acá va el URL base del consulado
    driver.get("https://www.exteriores.gob.es/Consulados/rosario/es/Comunicacion/Noticias/Paginas/Articulos/Instrucciones-para-solicitar-cita-previa.aspx")
    time.sleep(3)
    #Busca hipervínculo SACAR CITA y lo clickea.
    sacarCitaBtn = driver.find_element(By.CSS_SELECTOR, 'a[href="https://www.citaconsular.es/es/hosteds/widgetdefault/2bc271dfe25b4c2dc909d105a21abff93"]')
    sacarCitaBtn.click()
    time.sleep(3)
    #Busca botón CAPTCHA y lo clickea en un segundo rándom entre 2 y 5 para lograr pasar el captcha.
    captchaBtn = driver.find_element(By.CSS_SELECTOR, '#idCaptchaButton')
    time.sleep(round(random.uniform(1,4),1))
    captchaBtn.click()
    time.sleep(25)

    #Evalúa si en el html de la web encuentra "No hay horas disponibles", si encuentra eso no hace nada y se va del script, sino encuentra, envía un mail.
    if "No hay horas disponibles" in driver.page_source:
        driver.quit()
    else:
        # send_email()
        await enviar_mensaje()
        driver.quit()



#Este método ejecuta el script de turno y luego espera 120 segundos.
async def run_script_turno():
    while True:
        await script_turno()
        await asyncio.sleep(120)

if __name__ == '__main__':
    asyncio.run(run_script_turno())
