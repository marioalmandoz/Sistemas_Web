from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import base64
from bs4 import BeautifulSoup
import requests
import sys
import urllib



metodo = 'GET'
uri = 'https://xceed.me/es/san-sebastian/club/bataplan'
cabeceras = {'Host': 'xceed.me',
            'Content-Type': 'application/x-www-form-urlencoded'}
#cuerpo = {'abi_ize': sys.argv[1]}
#cuerpo_encoded = urllib.parse.urlencode(cuerpo)
#cabeceras['Content-Length'] = str(len(cuerpo_encoded))
respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

codigo = respuesta.status_code
descripcion = respuesta.reason
print(str(codigo) + " " + descripcion)
html = respuesta.content
print(html)
# abrir el navegador
browser = webdriver.Firefox()
# abrir la pagina
browser.get(uri)
element= browser.find_element(By.TAG_NAME,"a")

#element.click()
# esperar hasta que se hayan renderizado los elementos que nos interesan (timeout=30s)
#WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rg_i.Q4LuWd")))
# obtener el código HTML
#html = browser.page_source
# cerrar el navegador
browser.close()
print("Esto es lo que se imprime del tag_name: "+str(element.find_element('href')))