import urllib.parse
import requests
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json

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
print("\tStatus: " + str(status))

# Google responds to this request by returning a JSON object
# that contains a short-lived access token and a refresh token.
contenido = respuesta.text
print("\tCotenido:")
print(contenido)
contenido_json = json.loads(contenido)
access_token = contenido_json['access_token']
print("\taccess_token: " + access_token)


print("\nStep 6.- Calling Google APIs")
# Calendar API: https://developers.google.com/calendar/v3/reference
# CalendarList: https://developers.google.com/calendar/v3/reference#CalendarList
# CalendarList:list: https://developers.google.com/calendar/v3/reference/calendarList/list
uri = 'https://www.googleapis.com/calendar/v3/users/me/calendarList'
cabeceras = {'Host': 'www.googleapis.com',
             'Authorization': 'Bearer ' + access_token}
datos = {}
respuesta = requests.get(uri, headers=cabeceras, data=datos, allow_redirects=False)
status = respuesta.status_code
print("\tStatus: " + str(status))
contenido = respuesta.text
print("\tContenido:")
print(contenido)

contenido_dict = json.loads(contenido)
for each in contenido_dict['items']:
    print(each['summary'])
    print(each['id'])
    calendarioID = each['id']

calendarioID ="marioalmandoz6@gmail.com"
cabeceras = {}
cabeceras['User-Agent'] = 'Python Client'
cabeceras['Authorization'] = 'Bearer ' + access_token

url = 'https://www.googleapis.com/calendar/v3/calendars/' + calendarioID + '/events'
print(url)

respuesta = requests.get(url, headers=cabeceras)

print(str(respuesta.status_code)+' '+ str(respuesta.reason))
json_respuesta = json.loads(respuesta.content)
print("\nLista de Eventos")
for evento in json_respuesta['items']:
    print('-id: ' + evento['id'])
    if evento.get('summary'):
        print('summary: '+evento['summary'])




cabeceras = {}
cabeceras['User-Agent'] = 'Python Client'
cabeceras['Authorization'] = 'Bearer ' + access_token

url = 'https://www.googleapis.com/calendar/v3/calendars/' + calendarioID + '/events'
print(url)

cuerpo = {'end' : {'date':'2023-05-16'},
          'start': {'date':'2023-05-15'},
          'description':'Sistemas Web',
          'summary': 'Mensaje Creado'}
cuerpo= json.dumps(cuerpo)
respuesta = requests.post(url,headers=cabeceras, data=cuerpo)
print(respuesta.status_code)
print(respuesta.reason)
print(respuesta.content)
print(respuesta.request.headers)

