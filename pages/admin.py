from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Page)
admin.site.register(Juego)
admin.site.register(Detalle_Juego)
admin.site.register(Game)
admin.site.register(Game_Detail)

title = "Administracion de TodoGames"
subtitle = "TodoGames lo mas grande"
admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle