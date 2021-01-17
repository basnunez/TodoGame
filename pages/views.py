from django.shortcuts import render
from .models import Page, Juego, Detalle_Juego, Game, Game_Detail
from django.shortcuts import render, HttpResponse, redirect
import sqlite3
from lxml import html
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import urllib.request as urllib2
from .forms import FormJuego
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from TodoGames import actualizar

# Create your views here.

def page(request, slug):

    page = Page.objects.get(slug=slug)

    return render(request, "pages/page.html", {
        "page": page
    })

@login_required(login_url="login")
def guardar_full_juego (request):

    if request.method == 'POST':
        formulario = FormJuego(request.POST)

        if formulario.is_valid():
            data_form = formulario.cleaned_data

            encabezados = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
            }

            zmart = data_form.get('enlace')
            microplay = data_form.get('enlace2')
            weplay = data_form.get('enlace3')

            try:
                respuesta = requests.get(zmart, headers=encabezados)
                parserZmart = html.fromstring(respuesta.text)
                precioZmart = parserZmart.xpath("//div[@id='PriceProduct']/text()")
                precioZmart.pop(0)
                funciona = ''.join(precioZmart)
                precioZmart = funciona.replace(".", "")
                precioZmart = int(precioZmart)
            except Exception as e: 
                messages.warning(request, f'<h3>Error al extraer desde Zmart: {e}</h3>')
                return redirect ('juegos')
            #---zmart
            #---titulo, id y descripcion
            try:
                titulo = parserZmart.xpath("//div[@id='ficha_producto_int']/h1/text()")
                eliminarEspacios = ''.join(titulo)
                titulo = eliminarEspacios.replace("\r\n\r\n\r\n\t\t\t\t\t", "")
                idJuego = parserZmart.xpath("//span[@class='txValueInfoGral zmart__sku']/text()")
                idJuego = idJuego[0]
                desc = parserZmart.xpath("//span[@class='CPprodDet']/p/text()")
                desc = str(desc)
                desc = desc[2:]
                desc = desc[:-2]
            except Exception as e:
                messages.warning(request, f'<h3>Error al extraer desde Zmart: {e}</h3>')
                return redirect ('juegos') 
            #---titulo, id y descripcion
            juego = Juego(
                nombre = titulo,
                cod_juego = idJuego,
                tienda = 'Zmart',
                precio = precioZmart,
                enlace = zmart,
            )
            #---FIN ZMART
            #---microplay
            try:  
                respuesta = requests.get(microplay, headers=encabezados)
                parserMicroplay = html.fromstring(respuesta.text)
                precioMicroplay = parserMicroplay.xpath("//span[@class='text_web']/strong/text()")
                precioMicroplay = precioMicroplay[1]
                funciona = ''.join(precioMicroplay)
                precioMicroplay = funciona.replace(".", "")
                precioMicroplay = int(precioMicroplay)
            except Exception as e:
                messages.warning(request, f'<h3>Error al extraer desde Microplay: {e}</h3>')
                return redirect ('juegos')
            #---microplay
            #---imagen
            try:
                soup = BeautifulSoup(urllib2.urlopen(microplay).read(),"lxml")
                link = soup.find(itemprop="image")
                link_img = (link["src"])
                link_img = str(link_img)
            except Exception as e: 
                messages.warning(request, f'<h3>Error al extraer desde Microplay: {e}</h3>')
                return redirect ('juegos')
            #---imagen
            juego = Juego(
                nombre = titulo,
                cod_juego = idJuego,
                tienda = 'Microplay',
                precio = precioMicroplay,
                enlace = microplay,
            )
            #---FIN MICROPLAY
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
                messages.warning(request, f'<h3>Error al extraer desde Weplay: {e}</h3>')
                return redirect ('juegos')
            #---weplay
            updated_at = datetime.now()
            precios = [precioZmart, precioMicroplay, precioWeplay]
            ordenados = sorted(precios)
            game = Game(
                nombre = titulo,
                cod_juego = idJuego,
                tienda1 = 'Zmart',
                tienda2 = 'Microplay',
                tienda3 = 'Weplay',
                precio1 = precioZmart,
                precio2 = precioMicroplay,
                precio3 = precioWeplay,
                preciomasbajo = ordenados[0],
                enlace1 = zmart,
                enlace2 = microplay,
                enlace3 = weplay,
                desc = desc,
                link_imagen = link_img,
                created_at = updated_at,
                updated_at = updated_at
            )
            game.save()
            #---prueba
            messages.success(request, f'<h3>Se ha ingresado con exito el producto: {juego.nombre}</h3>')

            return redirect ('juegos')
        else:
                messages.warning(request, f'<h3>Error</h3>')
                return redirect ('juegos')
    else:
        formulario = FormJuego()
    

    return render(request, 'create_full_juego.html', {
        'form': formulario
    })

def borrar_juego (request, id):

    juego = Juego.objects.get(pk=id)
    juego.delete()

    return redirect ('juegos3')

@login_required(login_url="login")
def delete_game (request, id):
    game = Game.objects.get(pk=id)
    game.delete()

    return redirect ('juegos')

@login_required(login_url="login")
def juegos (request):

    search_term=''

    if 'search' in request.GET:
        search_term = request.GET['search']
        games = Game.objects.filter(Q(nombre__icontains=search_term))
        paginator = Paginator(games, 10)
    else:
        games = Game.objects.all()
        games = Game.objects.order_by('-updated_at')
        paginator = Paginator(games, 4)
    
    page = request.GET.get('page')
    page_games = paginator.get_page(page)

    context = {
        'title': 'Listado de Juegos',
        'games': page_games,
        'search_term': search_term
    }

    return render(request, "juegos3.html", context)

def games (request):

    search_term=''

    if 'search' in request.GET:
        search_term = request.GET['search']
        games = Game.objects.filter(Q(nombre__icontains=search_term))
        paginator = Paginator(games, 10)
    else:
        games = Game.objects.all()
        games = Game.objects.order_by('-updated_at')
        paginator = Paginator(games, 3)

    page = request.GET.get('page')
    page_games = paginator.get_page(page)

    context = {
        'games': page_games,
        'search_term': search_term
    }

    return render(request, "juegos.html", context)

@login_required(login_url="login")
def actualizarJuegos(request):
    try:
        actualizar.actualizarGames()
        messages.success(request, f'<h3>Se han actualizado los productos</h3>')
        return redirect ('juegos')
    except Exception as e:
        messages.warning(request, f'<h3>Error: {e}</h3>')
        return redirect ('juegos')
    


def cod_ps4 (request):
    games = Game.objects.filter(cod_juego="PS4G1764").order_by('precio1').order_by('precio2').order_by('precio3')

    return render(request, "paginas-juegos/cod-ps4.html",{
        'games' : games
    })

