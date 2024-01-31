import urllib.parse
import requests
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json

auth_code = ""

apy_key = "rycnjgixchjq962"
api_secret = "r3hx7xm94b2o30j"
redirect_uri= "http://localhost:8090"


print("\nStep 2.- Send a request to Google's OAuth 2.0 server")
servidor= 'www.dropbox.com'
uri = "https://accounts.google.com/o/oauth2/v2/auth"
datos = { 'client_id': apy_key,
          'redirect_uri': redirect_uri,
          'response_type': 'code'}
datos_encoded = urllib.parse.urlencode(datos)
recurso = '/oauth2/authorize?' + datos_encoded
uri = 'https://' + servidor+recurso

print("\tOpenning browser...")
webbrowser.open_new ((uri))

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localHost', 8090))
server_socket.listen(1)
print("\tLocal server listening on port 8090")

# Recibir la solicitude 302 del navegador
client_connection, client_address = server_socket.accept()
peticion = client_connection.recv(1024)
print("\tRequest from the browser received at local server:")

# Buscar en la petición el "auth_code"
primera_linea = peticion.decode('UTF8').split('\n')[0]
aux_auth_code = primera_linea.split(' ')[1]
auth_code = aux_auth_code[7:].split('&')[0]
print ("\tauth_code: " + auth_code)

# Devolver una respuesta al usuario
http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                "<html>" \
                "<head><title>Prueba</title></head>" \
                "<body>The authentication flow has completed. Close this window.</body>" \
                "</html>"
client_connection.sendall(http_response.encode(encoding="utf-8"))
client_connection.close()
server_socket.close()

datos = {'code': auth_code,
          'client_id': apy_key,
          'client_secret': api_secret,
          'redirect_uri': redirect_uri,
          'grant_type': 'authorization_code'}

cabeceras = {'User-Agent':'Python Client',
             'Content-Type': 'application/x-www-form-urlencoded'}

uri = 'https://api.dropboxapi.com/oauth2/token'
respuesta = requests.post(uri,headers=cabeceras,data=datos)

print(respuesta.status_code)
json_respuesta = json.loads(respuesta.content)
access_token = json_respuesta['access_token']
print("Access_Token: " + access_token)

######folder#########################
print("/list_folder")


uri = 'https://api.dropboxapi.com/2/files/list_folder'
path= ''
datos = {'path': path}
datos_encoded = json.dumps(datos)


print("Datuak: " + datos_encoded)
cabeceras = {'Host': 'api.dropboxapi.com',
           'Authorization': 'Bearer ' + access_token,
           'Content-Type': 'application/json'}
respuesta = requests.post(uri, headers=cabeceras, data=datos_encoded,allow_redirects=False)


status = respuesta.status_code
print ("\tStatus: " + str(status))
contenido = respuesta.content
print(contenido)

##### Subir un fichero
print("/subir fichero")
file_path='D:\Documentos\Prueba.txt'
with open(file_path, "r") as archivo:
    file_data = archivo.read()

uri = 'https://content.dropboxapi.com/2/files/upload'
dropbox_api_arg = {'path': "/prueba.txt",
                   'mode': 'add',
                   'autorename':True,
                    'mute': False}
dropbox_api_arg_json = json.dumps(dropbox_api_arg)
print("Dropbox_api_arg"+dropbox_api_arg_json)
cabeceras = {'Host': 'content.dropboxapi.com',
             'Authorization': 'Bearer '+ access_token,
             'Dropbox-API-Arg': dropbox_api_arg_json,
             'Content-Type': 'application/octet-stream'}
respuesta = requests.post(uri, headers=cabeceras,data=file_data, allow_redirects=False)

status = respuesta.status_code
print ("\tStatus: " + str(status))
contenido = respuesta.text
print(contenido)



####Borrar un archivo
print("/delete.file")

uri = 'https://api.dropboxapi.com/2/files/delete_v2'
datos = {'path': '/prueba.txt'}
datos_encoded = json.dumps(datos)
print('datos: '+ datos_encoded)
cabeceras = {'Host': 'api.dropboxapi.com',
             'Authorization': 'Bearer '+ access_token,
             'Content-Type': 'application/json'}
respuesta = requests.post(uri, headers=cabeceras, data=datos_encoded, allow_redirects=False)

status = respuesta.status_code
print("\tStatus: "+ str(status))


### descargar un archivo

print("/dawnload_file")
dropbox_api_arg = {'path': '/SW_2023_04_28 DropBox.pdf'}
dropbox_api_arg_json = json.dumps(dropbox_api_arg)
uri = 'https://content.dropboxapi.com/2/files/download'
cabeceras = {'Host': 'content.dropboxapi.com',
             'Authorization': 'Bearer '+ access_token,
             'Dropbox-API-Arg': dropbox_api_arg_json}
respuesta = requests.post(uri, headers=cabeceras, allow_redirects=False)

status = respuesta.status_code
print("\tStatus: "+ str(status))
#print(respuesta.content)
file_path = "prueba.pdf"
with open(file_path, "wb") as archivo:
    archivo.write(respuesta.content)
