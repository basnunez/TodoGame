from django.shortcuts import render
from blog.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def  list(request):

    articles = Article.objects.all()

    return render(request, 'articles/list.html',{
        'title': 'Articulos',
        'articles': articles
    })
