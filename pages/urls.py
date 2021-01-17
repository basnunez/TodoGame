from django.urls import path
from . import views

urlpatterns = [
        path('pagina/<str:slug>', views.page, name="page"),
        path('create-full-juego/', views.guardar_full_juego, name="guardar_full"),
        path('borrar-juego/<int:id>', views.borrar_juego, name="borrar"),
        path('delete-game/<int:id>', views.delete_game, name="delete"),
        path('actualizar/', views.actualizarJuegos, name="actualizar"),
        path('juegos/', views.games, name="juegos"),
        path('juegos3/', views.juegos, name="juegos3"),
        path('cod-ps4/', views.cod_ps4, name="cod-ps4"),
]

