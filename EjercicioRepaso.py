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
uri = 'https://websistemak-httptest.appspot.com/'
cabeceras = {'Host': 'websistemak-httptest.appspot.com',
            'Content-Type': 'application/x-www-form-urlencoded'}
#cuerpo = {'abi_ize': sys.argv[1]}
#cuerpo_encoded = urllib.parse.urlencode(cuerpo)
#cabeceras['Content-Length'] = str(len(cuerpo_encoded))
respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

codigo = respuesta.status_code
descripcion = respuesta.reason
print(str(codigo) + " " + descripcion)
html = respuesta.content
cuestionario  = respuesta.headers['location']
print(cuestionario)

metodo = 'GET'
uri = cuestionario
cabeceras = {'Host': 'websistemak-httptest.appspot.com',
            'Content-Type': 'application/x-www-form-urlencoded'}
#cuerpo = {'abi_ize': sys.argv[1]}
#cuerpo_encoded = urllib.parse.urlencode(cuerpo)
#cabeceras['Content-Length'] = str(len(cuerpo_encoded))
respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

codigo = respuesta.status_code
descripcion = respuesta.reason
print(str(codigo) + " " + descripcion)
html = respuesta.content
#print(html)
#print(respuesta.text)

metodo = 'POST'
uri = 'https://websistemak-httptest.appspot.com/processForm'
cabeceras = {'Host': 'websistemak-httptest.appspot.com',
            'Content-Type': 'application/x-www-form-urlencoded'}
cuerpo = "erantzuna=a&erantzuna=b&erantzuna=c"
respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)

codigo = respuesta.status_code
descripcion = respuesta.reason
print(str(codigo) + " " + descripcion)
#print(respuesta.text)
uri_siguiente = respuesta.headers['location']
print(uri_siguiente)

metodo = 'GET'
uri = uri_siguiente
print()
cabeceras = {'Host': 'websistemak-httptest.appspot.com'}
respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

codigo = respuesta.status_code
descripcion = respuesta.reason
print(str(codigo) + " " + descripcion)
html = respuesta.content
#print(html)
#print(respuesta.text)

# abrir el navegador
browser = webdriver.Firefox()
# abrir la pagina
uri = uri_siguiente
browser.get(uri)
# esperar hasta que se hayan renderizado los elementos que nos interesan (timeout=30s)
WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
# obtener el código HTML
html = browser.page_source
# cerrar el navegador
browser.close()

# instanciar un parser para html y cargar en memoria el DOM del html
# “soup" es una ref. al elemento raíz del DOM
document = BeautifulSoup(html, 'html.parser')

# buscar en el DOM todos aquellos elementos cuyo atributo "class" valga "rg_i Q4LuWd"
img_results = document.find_all('img')
#print(img_results)
each = img_results[0]
if each.has_attr('src'):
    src = each['src']
else:
    src = each['data-src']
print("matrixPic" + src)
img = None
if src.find("data:image") != -1:
    # data:[<mime type>][;charset=<charset>][;base64],<encoded data>
    img = base64.b64decode(src.replace("data:image/png;base64,", ""))
else:
    res = requests.get(src)
    img = res.content
file = open("./matrixImg/matrixPic1.png", "x+b")
file.write(img)
file.close()


