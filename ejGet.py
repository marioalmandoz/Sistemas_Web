import requests
import urllib
import sys

metodo= 'GET'
uri_base= "http://gae-sw-2017.appspot.com/processForm"
cabeceras= {'Host': 'gae-sw-2017.appspot.com'}
query = {'dni': sys.argv[1]}
query_encoded = urllib.parse.urlencode(query)
uri = uri_base + '?' + query_encoded
respuesta = requests.request(metodo,uri,headers=cabeceras,allow_redirects=False)

codigo = respuesta.status_code
descripcion = respuesta.reason
print(str(codigo) + " " + descripcion)
for cabeceras in respuesta.headers:
    print(cabeceras+ ": " + respuesta.headers[cabeceras])
cuerpo = respuesta.content
print(cuerpo)