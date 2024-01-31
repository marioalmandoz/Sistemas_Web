import base64
import msvcrt
import csv
from bs4 import BeautifulSoup
import requests
import sys
import urllib
import getpass

'''
Mario Almandoz Latierro
Sistemas web G1
13/03/2023
Python G1
Es un archivo .py que accede a egela, a la asignatura de Sistemas web
y descarga todos los pdf's y busca las tareas a realizar y escribe su fecha de entrega 
y su uri en un fichero .csv 
'''




usuario = sys.argv[1]
nombre = sys.argv[2]
password =getpass.getpass("ingresa la contraseña ")

#PRIMERA PETICION
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
metodo = 'POST'
uri = uri_siguiente
print(metodo)
print(uri)
cabeceras = {'Host': 'egela.ehu.eus',
            'Content-Type': 'application/x-www-form-urlencoded',
             'Cookie': moodle_sesion}
cuerpo = {'logintoken': logintoken,
          'username': usuario,
          'password': password}
cuerpo_encoded = urllib.parse.urlencode(cuerpo)
cabeceras['Content-Length'] = str(len(cuerpo_encoded))
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
    metodo= 'GET'
    uri = uri_siguiente
    print(metodo)
    print(uri)
    cabeceras = {'Host': 'egela.ehu.eus',
                 'Cookie': moodle_sesion}
    respuesta = requests.request(metodo,uri, headers=cabeceras, allow_redirects=False)

    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print(str(codigo) + " " + descripcion)

    html = respuesta.content
    datos = BeautifulSoup(html, 'html.parser')
    uri_siguiente = datos.find_all('a')[0]['href']
    print("Este es el location de la tercera peticion: ", respuesta.headers['location'])
    print("\n")
    #ESTA ES LA CUARTA PETICION
    metodo= 'GET'
    uri = uri_siguiente
    print(metodo)
    print(uri)
    cabeceras = {'Host': 'egela.ehu.eus',
                 'Cookie': moodle_sesion}
    respuesta = requests.request(metodo,uri, headers=cabeceras, allow_redirects=False)

    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print(str(codigo) + " " + descripcion)

    html = respuesta.content.decode('UTF-8')
    pos=html.find(nombre)#ESTO DA LA POSICION DE DONDE ESTA ESE STRING
    if pos==-1:
        sys.exit(0)
    else:
        print("El usuario es correcto")
        print("pulse cualquier tecla para continuar")
        msvcrt.getch()

    html = respuesta.content
    datos = BeautifulSoup(html, 'html.parser')
    uri_siguiente = datos.find_all('a',{'class': 'ehu-visible'})[0]['href']


    #QUINTA PETICION
    metodo = 'GET'
    uri = uri_siguiente
    print(metodo)
    print(uri)
    cabeceras = {'Host': 'egela.ehu.eus',
                 'Cookie': moodle_sesion}
    respuesta = requests.request(metodo,uri, headers=cabeceras, allow_redirects=False)

    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print(str(codigo) + " " + descripcion)

    #ESTA PARTE DE CODIGO ES PARA CONSEGUIR LOS PDF'S
    html = respuesta.content
    datos = BeautifulSoup(html, 'html.parser')
    uri_imagen_pdf = datos.find_all('img',{'class':'iconlarge activityicon'})[3]['src']
    uri_pdf = datos.find_all('img',{'src':uri_imagen_pdf})
    print("Esta es la uri de la imagen de los pdf: ",uri_imagen_pdf)


    #ESTA PARTE DE CODIGO ES PARA CONSEGUIR LO DE LAS TAREAS
    uri_imagen_entrega = datos.find_all('img',{'class':'iconlarge activityicon'})[37]['src']
    print("Esta es la uri de la imagen de las entregas: ",uri_imagen_entrega)
    uri_tareas = datos.find_all('img',{'src':uri_imagen_entrega})
    print(uri_tareas[1].parent['href'])

    with open('Tareas.csv', 'a') as csv_file:
        for t in range(len(uri_tareas)):
            try:
                uri_siguiente_tarea = uri_tareas[t].parent['href']
            except KeyError:
                print("Esta tarea no esta disponible",t)
            else:
                #Peticion Tareas
                print("PETICION DE LA TAREA")
                metodo = 'GET'
                uri = uri_siguiente_tarea
                print(metodo)
                print(uri)
                cabeceras = {'Host': 'egela.ehu.eus',
                             'Cookie': moodle_sesion}
                respuesta = requests.request(metodo,uri, headers=cabeceras, allow_redirects=False)

                codigo = respuesta.status_code
                descripcion = respuesta.reason
                print(str(codigo) + " " + descripcion)

                html_tarea = respuesta.content
                tarea = BeautifulSoup(html_tarea, 'html.parser')
                print(tarea.find('td',{'class':'cell c1 lastcol'}).text)
                fecha_entrega = tarea.find('td',{'class':'cell c1 lastcol'}).text


                csv_file.write(f'fecha de entrega,{fecha_entrega},Esta es la uri de la tarea, {uri_siguiente_tarea}\n')
    csv_file.close()

#Codigo para conseguir los pdfs

    for i in range(len(uri_pdf)):
        uri_siguiente = uri_pdf[i].parent['href']
        nombre_pdf = str(uri_pdf[i].parent.span).split('>')[1].split('<')[0]
    #PRIMERA PETICION PDF
        print("Esta es la primera peticion del pdf"+str(i))
        metodo = 'GET'
        uri = uri_siguiente
        print(metodo)
        print(uri)
        cabeceras = {'Host': 'egela.ehu.eus',
                     'Cookie': moodle_sesion}
        respuesta = requests.request(metodo,uri, headers=cabeceras, allow_redirects=False)

        codigo = respuesta.status_code
        descripcion = respuesta.reason
        print(str(codigo) + " " + descripcion)
        uri_siguiente= respuesta.headers['location']

        #SEGUNDA PETICION PDF
        print("Esta es la segunda peticion del pdf"+str(i))
        metodo = 'GET'
        uri = uri_siguiente
        print(metodo)
        print(uri)
        cabeceras = {'Host': 'egela.ehu.eus',
                     'Cookie': moodle_sesion}
        respuesta = requests.request(metodo,uri, headers=cabeceras, allow_redirects=False)

        codigo = respuesta.status_code
        descripcion = respuesta.reason
        print(str(codigo) + " " + descripcion)



        pdf = base64.b64decode(respuesta.content)
        with open('./pdf/'+nombre_pdf+'.pdf', 'wb') as pdf_file:
            pdf_file.write(respuesta.content)



