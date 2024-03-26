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

#Este método envía un correo electrónico a los usuarios indicados en "recipient_email" usando SMTP.
def send_email():
    sender_email, sender_password = leerCredencialesDeCorreo()
    recipient_email = leerCorreoParaEnviar()
    subject = "HAY TURNOS!"
    body = "WEB TURNOS https://www.citaconsular.es/es/hosteds/widgetdefault/24dc3ade850068f20d7c19845f023121c . CREDS JUANI: RE202401399336  JGF22101992  .  CREDS MAQUI: MGF26121995   RE202401401336  .  CREDS CLAU: CFP02091965   RE202401406336"
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
    driver.get("https://www.exteriores.gob.es/Consulados/rosario/es/Comunicacion/Noticias/Paginas/Articulos/Instrucciones-cita-previa-solicitud-pasaporte.aspx")
    time.sleep(3)
    #Busca hipervínculo SACAR CITA y lo clickea.
    sacarCitaBtn = driver.find_element(By.CSS_SELECTOR, 'a[href="https://www.citaconsular.es/es/hosteds/widgetdefault/24dc3ade850068f20d7c19845f023121c"]')
    sacarCitaBtn.click()
    time.sleep(30)

    #Evalúa si en el html de la web encuentra "No hay horas disponibles", si encuentra eso no hace nada y se va del script, sino encuentra, envía un mail.
    if "No hay horas disponibles" in driver.page_source:
        driver.quit()
    else:
        # send_email()
        await send_email()
        driver.quit()



#Este método ejecuta el script de turno y luego espera 120 segundos.
async def run_script_turno():
    while True:
        await script_turno()
        await asyncio.sleep(130)

if __name__ == '__main__':
    asyncio.run(run_script_turno())