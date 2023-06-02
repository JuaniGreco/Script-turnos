from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import smtplib
import os
from selenium.webdriver.firefox.service import Service
import time
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText

def leerCredencialesDeCorreo():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    directorio_padre = os.path.abspath(os.path.join(directorio_actual, os.pardir))
    archivoCredenciales = os.path.join(directorio_padre, "credencialesCorreo.txt")
    with open(archivoCredenciales, "r") as file:
        lines = file.readlines()
        sender_email = lines[0].strip()
        sender_password = lines[1].strip()
    return sender_email, sender_password

def send_email():
    sender_email, sender_password = leerCredencialesDeCorreo()
    recipient_email = ["juanigreco22@gmail.com", "delfiigreco@gmail.com", "julietaoldani06@gmail.com"]
    subject = "HAY TURNOS!"
    body = "https://www.exteriores.gob.es/Consulados/rosario/es/Comunicacion/Noticias/Paginas/Articulos/Instrucciones-para-solicitar-cita-previa.aspx \n37.153.076\n1t8bS1d554"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_email)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())

def script_turno():
    gecko_driver_path = r"C:\firefox_webdriver\geckodriver.exe"
    driver = webdriver.Firefox(service=Service(gecko_driver_path))
    driver.get("https://www.exteriores.gob.es/Consulados/rosario/es/Comunicacion/Noticias/Paginas/Articulos/Instrucciones-para-solicitar-cita-previa.aspx")
    time.sleep(1)
    sacarCitaBtn = driver.find_element(By.CSS_SELECTOR, 'a[href="https://www.citaconsular.es/es/hosteds/widgetdefault/2bc271dfe25b4c2dc909d105a21abff93"]')
    sacarCitaBtn.click()
    time.sleep(1)
    captchaBtn = driver.find_element(By.CSS_SELECTOR, '#idCaptchaButton')
    time.sleep(round(random.uniform(2,5),1))
    captchaBtn.click()
    time.sleep(20)

    if "No hay horas disponibles" in driver.page_source:
        send_email()
        driver.quit()
    else:
        send_email()
        driver.quit()

script_turno()

time.sleep(120)

while True:
    script_turno()
    time.sleep(120)