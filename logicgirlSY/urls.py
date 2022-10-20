from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from app_posts.views import Home, Jogos, Publicacoes, Perfil, Post, EditarPost

urlpatterns = [
    path('',Home,name="Home"),
    path('Jogos/',Jogos,name="Jogos"),
    path('Post/',Publicacoes,name="Publicacoes"),
    path('Post/<str:uid>',Post,name="Post"),
    path('EditarPost/<str:uid>',EditarPost,name="EditarPost"),
    path('Perfil/<str:user>',Perfil,name="Perfil"),
    path('admin/', admin.site.urls),
    path('u/',include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
