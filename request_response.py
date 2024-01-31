import requests
import sys
import zlib

metodo='GET'
uri="http://www.google.es/"
cabeceras={'Host':'www.google.es'}
compressed= False
if len(sys.argv)==1:
    cabeceras['Accept-Encoding']= 'identity'
elif sys.argv[1] == 'compress':
    compressed= True
    cabeceras['Accept-Encoding'] = 'gzip'
else:
    print("Error! Erabilera: python compression_es.py compress")
    exit(0)
#cuerpo='' esto es del codigo de alejandro
respuesta=requests.request(metodo, uri, headers=cabeceras, allow_redirects=False, stream=True)
#print(respuesta.status_code)

codigo=respuesta.status_code
descripcion=respuesta.reason
print(str(codigo) +" "+descripcion)
for cabecera in respuesta.headers:
    print(cabecera + ": "+respuesta.headers[cabecera])
print("RESPONSE CONTENT LENGTH: " + str(len(respuesta.raw.data)) + "byte")
if compressed:
    contenido_compressed = respuesta.raw.data
    contenido_uncompressed = zlib.decompress(contenido_compressed, 16+zlib.MAX_WBITS)
    print("UNCOMPRESSED RESPONSE CONTENT LENGTH: " + str(len(contenido_uncompressed)))
cuerpo=respuesta.content
print(cuerpo)

metodo='GET'
uri=respuesta.headers['Location']
cabeceras={'Host': uri.split('/')[2]}
cuerpo=''
respuesta=requests.request(metodo,uri,headers=cabeceras,data=cuerpo,allow_redirects=False)

codigo=respuesta.status_code
descripcion=respuesta.reason
print(str(codigo) +" "+descripcion)
for cabecera in respuesta.headers:
    print(cabecera + ": "+respuesta.headers[cabecera])
cuerpo=respuesta.content
print(cuerpo)

metodo='GET'
uri=respuesta.headers['Location']
cabeceras={'Host': uri.split('/')[2]}
cuerpo=''
respuesta=requests.request(metodo,uri,headers=cabeceras,data=cuerpo,allow_redirects=False)

codigo=respuesta.status_code
descripcion=respuesta.reason
print(str(codigo) +" "+descripcion)
for cabecera in respuesta.headers:
    print(cabecera + ": "+respuesta.headers[cabecera])
cuerpo=respuesta.content
print(cuerpo)