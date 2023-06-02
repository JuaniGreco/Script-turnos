import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import smtplib
import os

def leerCredencialesDeCorreo():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    directorio_padre = os.path.abspath(os.path.join(directorio_actual, os.pardir))
    archivoCredenciales = os.path.join(directorio_padre, "credenciales.txt")
    with open(archivoCredenciales, "r") as file:
        lines = file.readlines()
        sender_email = lines[0].strip()
        sender_password = lines[1].strip()
    return sender_email, sender_password

def send_email():
    sender_email, sender_password = leerCredencialesDeCorreo()
    recipient_email = "juanigreco22@gmail.com"
    subject = "HAY TURNOS!"

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        message = f"Subject: {subject}\n\n"
        server.sendmail(sender_email, recipient_email, message)
        server.close()

def script_turno():

    driver = webdriver.Firefox(executable_path="C:\firefox_webdriver/geckodriver.exe")
    driver.get("https://www.exteriores.gob.es/Consulados/rosario/es/Comunicacion/Noticias/Paginas/Articulos/Instrucciones-para-solicitar-cita-previa.aspx")
    time.sleep(1)
    sacarCitaBtn = driver.find_element_by_link_text('SACAR CITA')
    sacarCitaBtn.click()
    time.sleep(1)
    captchaBtn = driver.find_element_by_id('idCaptchaButton')
    time.sleep(round(random.uniform(1,3),1))
    captchaBtn.click()

    if "No hay horas disponibles" in driver.page.source:
        driver.quit()
    else:
        send_email()

schedule.every(2).minutes.do(script_turno)

while True:
    schedule.run_pending()
    time.sleep(1)