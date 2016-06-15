# -*- coding: utf-8 -*-


import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.
import time # Librería para hacer que el programa que controla el bot no se acabe.

import requests
import json
 
TOKEN = '126754070:AAHFg1a9ABNMC0JeRH7mpNR9XH_LorEzK1E' # Nuestro tokken del bot (el que @BotFather nos dió).
 
bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.



lat = 0
lon = 0

libres = 'Estaciones proximas de Valenbisi con plazas libres'
disponibles = 'Estaciones proximas de Valenbisi con bicis disponibles'
parking = 'Aparcamientos publicos cercanos con plazas libres'
taxi = 'Paradas de taxis cercanas'

 
def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
    global lat
    global lon  
  
    for m in messages: # Por cada dato 'm' en el dato 'messages'
        
        
        if m.content_type == 'text':
            cid = m.chat.id # Almacenaremos el ID de la conversación.
            
            if lat == 0 or lon == 0:
                bot.send_message(cid,"Primero manda tu ubicación desde el icono de ")# + u'\U0001f4ce')
            else:    
                if m.text == disponibles:
                    obtener('valenbisi/disponibles',lat,lon,cid)
                    print "[" + str(cid) + "]: " + 'valenbisi disponibles'
               
                elif    m.text == libres: 
                    obtener('valenbisi/libres',lat,lon,cid)
                    print "[" + str(cid) + "]: " + 'valenbisi libres'
                elif    m.text == parking: 
                    obtener('aparcamientos',lat,lon,cid)
                    print "[" + str(cid) + "]: " + 'aparcamientos'
                elif    m.text == taxi: 
                    obtener('taxis',lat,lon,cid) 
                    print "[" + str(cid) + "]: " + 'taxis'
        
        if m.content_type == 'location':
            cid = m.chat.id 
            print "[" + str(cid) + "]: " + 'localizacion'
            bot.send_message(cid,"Ubicación actualizada")
           
            lat = (m.location.latitude) * 10**6
            lon = (m.location.longitude) * 10**6
            lat = int(lat)
            lon = int(lon)
            
            

 
bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.
 
bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo.


 
@bot.message_handler(commands=['prueba']) 
def command_prueba(m):  
    cid = m.chat.id
    bot.send_message(cid,lat)
    bot.send_message(cid,lon)    

 
@bot.message_handler(commands=['start']) # Indicamos que lo siguiente va a controlar el comando parking
def command_bisi(m): # Definimos una función que resuelva lo que necesitemos.
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(libres,disponibles,parking,taxi)
    
    bot.send_message(cid, "¿Qué buscas?:", reply_markup=markup)
    markup = types.ReplyKeyboardHide(selective=False)
    
    
    
    
def obtener(tipo,latitud,longitud,cid):
    
    url = 'http://mapas.valencia.es/lanzadera/gps/' + tipo + '/' + str(latitud)+ '/' + str(longitud) 
    r = requests.get(url, auth=('jcollado', 'FSwkOrUD'))

    json_object = r.json()
    parsed_data = json.dumps(json_object)

    lol = json.loads(parsed_data)
    for parkings in lol:
        lati = (parkings["latDestino"])/float(10**6)
        longi = (parkings["lonDestino"])/float(10**6)
        distan = "Distancia: " + str((parkings["distancia"])) +" m"
        mensa = (parkings["mensaje"])
        stringfinal = distan +"\n"+mensa
        
        
        bot.send_location( cid,lati,longi)
        bot.send_message( cid, stringfinal)
 
while True: # Ahora le decimos al programa que no se cierre haciendo un bucle que siempre se ejecutará.
    time.sleep(300) # Hacemos que duerma durante un periodo largo de tiempo para que la CPU no esté trabajando innecesáremente.
