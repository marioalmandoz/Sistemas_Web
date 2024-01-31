import urllib.parse
import requests
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json

from bs4 import BeautifulSoup

auth_code = ""
print("###################################")
print("OAuth 2.0 for Mobile & Desktop Apps")
print("###################################")
# https://developers.google.com/identity/protocols/oauth2/native-app

print("\nStep 1.- Prerequisites on Google Cloud Console")
print("\tEnable APIs for your project")
print("\tIdentify access scopes")
print("\tCreate authorization credentials")
print("\tConfigure OAuth consent screen")
print("\tAdd access scopes and test users")


client_id = "299861677320-0f48q92uieftd0js4bksbs2kcluss3hk.apps.googleusercontent.com"
client_secret = "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"

scope = "https://www.googleapis.com/auth/calendar.readonly"

scope = "https://www.googleapis.com/auth/calendar"

redirect_uri = "http://127.0.0.1:8090"

print("\nStep 2.- Send a request to Google's OAuth 2.0 server")
uri = "https://accounts.google.com/o/oauth2/v2/auth"
datos = { 'client_id': client_id,
          'redirect_uri': redirect_uri,
          'response_type': 'code',
          'scope': scope}
datos_encoded = urllib.parse.urlencode(datos)

print("\tOpenning browser...")
webbrowser.open_new ((uri +'?' + datos_encoded))

print("\nStep 3.- Google prompts user for consent")

print("\nStep 4.- Handle the OAuth 2.0 server response")

# Crear servidor local que escucha por el puerto 8090
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localHost', 8090))
server_socket.listen(1)
print("\tLocal server listening on port 8090")

# Recibir la solicitude 302 del navegador
client_connection, client_address = server_socket.accept()
print("Estos son client_adress: ",client_address, " conection: ",client_connection)
peticion = client_connection.recv(1024)
print("Esta es la peticion: ",peticion)
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

print("\nStep 5.- Exchange authorization code for refresh and access tokens")

uri = 'https://oauth2.googleapis.com/token'
cabeceras = {'Host': 'oauth2.googleapis.com',
             'Content-Type': 'application/x-www-form-urlencoded'}

datos = {'code': auth_code,
          'client_id': client_id,
          'client_secret': client_secret,
          'redirect_uri': redirect_uri,
          'grant_type': 'authorization_code'}
respuesta = requests.post(uri, headers=cabeceras, data=datos, allow_redirects=False)
status = respuesta.status_code
print("\tStatus: " + str(status)+" "+respuesta.reason)


# Google responds to this request by returning a JSON object
# that contains a short-lived access token and a refresh token.
contenido = respuesta.text
print("\tCotenido:")
print(contenido)
contenido_json = json.loads(contenido)
access_token = contenido_json['access_token']
print("\taccess_token: " + access_token)

#Peticiones adicionales para ralizar lo que se necesite en l aapi de google
#En este caso se crea un evento
print("\n step 6 create a new event")
scope = 'https://www.googleapis.com/auth/calendar'
calendarioID ="marioalmandoz6@gmail.com"
cabeceras = {}
cabeceras['User-Agent'] = 'Python Client'
# suponer que access_token se ha definido y obtenido correctamente antes
cabeceras['Authorization'] = 'Bearer ' + access_token
cabeceras['Content-Type'] = 'application/json'
url = 'https://www.googleapis.com/calendar/v3/calendars/'+calendarioID+'/events'
cuerpo = { 'end' : { 'date': '2022-05-29' },
            'start' : { 'date': '2022-05-28' },
            'description': 'Sistemas Web',
            'summary' : 'EXAMEN' }
cuerpo = json.dumps(cuerpo)
respuesta = requests.post(url, headers=cabeceras, data=cuerpo)
print(respuesta.status_code)
print(respuesta.reason)
print(respuesta.content)
'''
print("Primera peticion")
metodo = 'GET'
uri = "https://egela.ehu.eus/login/index.php"
print(metodo)
print(uri)
cabeceras = {'Host': 'egela.ehu.eus'}
respuesta = requests.request(metodo,uri, headers=cabeceras, allow_redirects=False)

codigo = respuesta.status_code
descripcion = respuesta.reason
print(str(codigo) + " " + descripcion)
moodle_sesion= respuesta.headers['Set-Cookie'].split(";",1)[0]
print("Este es el moodle_sesion: ",moodle_sesion)

html = respuesta.content
datos = BeautifulSoup(html, 'html.parser')
uri_siguiente = datos.find_all('form',{'class': 'm-t-1 ehuloginform'})[0]['action']
logintoken = datos.find_all('input', {'name': 'logintoken'})[0]['value']
print("Este es el logintoken: ",logintoken)
print("\n")

#SEGUNDA PETICION
print("Segunda peticion")
metodo = 'POST'
uri = uri_siguiente
print(metodo)
print(uri)
cabeceras = {'Host': 'egela.ehu.eus',
            'Content-Type': 'application/x-www-form-urlencoded',
             'Cookie': moodle_sesion}
cuerpo = {'logintoken': logintoken,
          'username': '1002336',
          'password': '10kgaGJ7'}
cuerpo_encoded = urllib.parse.urlencode(cuerpo)
cabeceras['Content-Length'] = str(len(cuerpo_encoded))
# Aqui si pones allow_redirects=True no haria falta hacer las siguientes peticiones, te lo redirige solo
respuesta = requests.request(metodo, uri, data=cuerpo_encoded, headers=cabeceras, allow_redirects=False)
codigo = respuesta.status_code
descripcion = respuesta.reason
print(cuerpo)
print(str(codigo) + " " + descripcion)
try:
    moodle_sesion= respuesta.headers['Set-Cookie'].split(";",1)[0]
except KeyError:
    print("Ha introducido mal la contraseña vuelva a ejecutar el programa")
else:
    print("Este es el moodle_sesion: ",moodle_sesion)

    html = respuesta.content
    datos = BeautifulSoup(html, 'html.parser')
    uri_siguiente = datos.find_all('a')[0]['href']
    print(uri_siguiente)
    print("Este es el location de la segunda peticion: ",respuesta.headers['location'])
    print("\n")

#TERCERA PETICION
    print("Tercera peticion")
    metodo= 'GET'
    uri = uri_siguiente
    print(metodo)
    print(uri)
    cabeceras = {'Host': 'egela.ehu.eus',
                 'Cookie': moodle_sesion}
    #Aqui si pones allow_redirects=True no haria falta hacer las siguientes peticiones, te lo redirige solo
    respuesta = requests.request(metodo,uri, headers=cabeceras, allow_redirects=False)

    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print(str(codigo) + " " + descripcion)


    html = respuesta.content
    datos = BeautifulSoup(html, 'html.parser')
    uri_siguiente = datos.find_all('a')[0]['href']
    print("Este es el location de la tercera peticion: ", respuesta.headers['location'])
    print("\n")'''
    #El codigo continuaria pero no lo pongo porque no es necesario para ver la comprobación
