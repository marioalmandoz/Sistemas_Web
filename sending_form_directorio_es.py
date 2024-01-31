#-*- coding: UTF-8 -*-
import requests
import sys
import urllib
from bs4 import BeautifulSoup


metodo = 'POST'
uri = 'https://www.ehu.eus//bilatu/buscar/sbilatu.php?lang=es1'
cabeceras = {'Host': 'www.ehu.eus',
            'Content-Type': 'application/x-www-form-urlencoded'}
cuerpo = {'abi_ize': sys.argv[1]}
cuerpo_encoded = urllib.parse.urlencode(cuerpo)
cabeceras['Content-Length'] = str(len(cuerpo_encoded))
respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo_encoded, allow_redirects=False)

codigo = respuesta.status_code
descripcion = respuesta.reason
print(str(codigo) + " " + descripcion)
html = respuesta.content
#print(html)

documento = BeautifulSoup(html, "html.parser")
#print(documento)

lista_Personas = documento.find_all('td',{'class': 'fondo_listado'})
#print(len(lista_Personas))
cont = 0
for persona in lista_Personas[:]:
    persona_enlace = persona.a['href']
    persona_nombre = persona.text.strip()
    print(str(cont)+"-"+ persona_nombre+" : https://www.ehu.eus"+persona_enlace)
    cont = cont + 1