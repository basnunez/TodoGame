import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request as urllib2
import requests
from lxml import html

def actualizarGames():
    conn = sqlite3.connect('C:/SeminarioGrado/TodoGames/db.sqlite3')
    c = conn.cursor()
    sql_query = """SELECT enlace1, enlace2, enlace3, nombre, precio1, precio2, precio3, preciomasbajo FROM pages_game """
    c.execute(sql_query)
    enlaces = c.fetchall()
    print("")
    print("\bEmpezando actualizacion de juegos")
    for enlace in enlaces:
        print(" ")
        print ("----",enlace[3],"------")
        print ("----",enlace[0],"------")
        print ("----",enlace[1],"------")
        print ("----",enlace[2],"------")
        print(" ")
        encabezados = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
            #--enlaces
        zmart = enlace[0]
        microplay = enlace[1]
        weplay = enlace[2]
            #--enlaces
            #---titulo, id y descripcion
        try:
                respuesta = requests.get(zmart, headers=encabezados)
                parserZmart = html.fromstring(respuesta.text)
                idJuego = parserZmart.xpath("//span[@class='txValueInfoGral zmart__sku']/text()")
                idJuego = idJuego[0]
                print(idJuego)
        except Exception as e: 
                print("Error: ",e)
            #---titulo, id y descripcion
            #---zmart
        try:
                precioZmart = parserZmart.xpath("//div[@id='PriceProduct']/text()")
                precioZmart.pop(0)
                funciona = ''.join(precioZmart)
                precioZmart = funciona.replace(".", "")
                precioZmart = int(precioZmart)
                print(precioZmart)
        except Exception as e: 
                print("Error: ",e)
            #---zmart
            #---weplay
        try:
            respuesta = requests.get(weplay, headers=encabezados)
            parserWeplay = html.fromstring(respuesta.text)
            precioWeplay = parserWeplay.xpath("//span[@class='price']/text()")

            if (len(precioWeplay) == 2):
                precioWeplay.pop(0)
            else:
                precioWeplay.pop(0)
                precioWeplay.pop(0)

            EliminarEspacios = ''.join(precioWeplay)
            precioWeplay = EliminarEspacios.replace("$", "")
            precioWeplay = precioWeplay.replace(".", "")
            precioWeplay = int(precioWeplay)
        except Exception as e: 
                print("Error: ",e)
            #---weplay
            #---microplay
        try:  
                respuesta = requests.get(microplay, headers=encabezados)
                parserMicroplay = html.fromstring(respuesta.text)
                precioMicroplay = parserMicroplay.xpath("//span[@class='text_web']/strong/text()")
                precioMicroplay = precioMicroplay[1]
                funciona = ''.join(precioMicroplay)
                precioMicroplay = funciona.replace(".", "")
                precioMicroplay = int(precioMicroplay)
                print(precioMicroplay)
                print(precioWeplay)
        except Exception as e: 
                print("Error: ",e)
            #---microplay
        updated_at = datetime.now()

        if precioZmart > enlace[4]:
            print("El precio nuevo es mas caro por",(precioZmart-enlace[4]), "pesos en Zmart")
        elif precioZmart < enlace[4]:
            print("El precio nuevo es mas barato por",(enlace[4]-precioZmart),"pesos en Zmart")
        else:
            print("No hay variacion de precio en Zmart")

        if precioMicroplay > enlace[5]:
            print("El precio nuevo es mas caro por",(precioMicroplay-enlace[5]), "pesos en Microplay")
        elif precioMicroplay < enlace[5]:
            print("El precio nuevo es mas barato por",(enlace[5]-precioMicroplay),"pesos en Microplay")
        else:
            print("No hay variacion de precio en Microplay")

        if precioWeplay > enlace[6]:
            print("El precio nuevo es mas caro por",(precioWeplay-enlace[6]), "pesos en Weplay")
        elif precioWeplay < enlace[6]:
            print("El precio nuevo es mas barato por",(enlace[6]-precioWeplay),"pesos en Weplay")
        else:
            print("No hay variacion de precio en Weplay")

        precios = [precioZmart, precioMicroplay, precioWeplay]
        ordenados = sorted(precios)
        masbajo = enlace[7]

        if ordenados[0] < masbajo:
            masbajo = ordenados[0]
            print("Ha bajado de precio en comparacion al mas bajo historico")

        try:
                sql_update_query = """Update pages_game set precio1 = ?, precio2 = ?, precio3 = ?, preciomasbajo = ?, updated_at = ? where cod_juego = ? """
                data = (precioZmart, precioMicroplay, precioWeplay, masbajo, updated_at, idJuego)
                c.execute(sql_update_query, data)
                conn.commit()
                print("Se actualizo corrrectamente")
        except Exception as e:
                print("Error: ",e)

    print(" ")
    print("Todos los juegos han sido actualizados")
    conn.close()