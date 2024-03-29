from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import base64
from bs4 import BeautifulSoup
import requests
import os
# abrir el navegador
browser = webdriver.Firefox()
# abrir la pagina
uri = "https://www.google.com/search?q=pinarello+f12&tbm=isch"
browser.get(uri)
element= browser.find_element(By.XPATH,"/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span")
element.click()
# esperar hasta que se hayan renderizado los elementos que nos interesan (timeout=30s)
WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rg_i.Q4LuWd")))
# obtener el código HTML
html = browser.page_source
# cerrar el navegador
browser.close()

# instanciar un parser para html y cargar en memoria el DOM del html
# “soup" es una ref. al elemento raíz del DOM
document = BeautifulSoup(html, 'html.parser')
# buscar en el DOM todos aquellos elementos cuyo atributo "class" valga "rg_i Q4LuWd"
img_results = document.find_all('img', {'class': 'rg_i Q4LuWd'})
print(img_results)

for idx, each in enumerate(img_results):
    src = ""
    if each.has_attr('src'):
        src = each['src']
    else:
        src = each['data-src']
    print(str(idx) + " " + src)
    img = None
    if src.find("data:image") != -1:
        # data:[<mime type>][;charset=<charset>][;base64],<encoded data>
        img = base64.b64decode(src.replace("data:image/jpeg;base64,", ""))
    else:
        res = requests.get(src)
        img = res.content
    file = open("./img/" + str(idx) + ".jpeg", "x+b")
    file.write(img)
    file.close()