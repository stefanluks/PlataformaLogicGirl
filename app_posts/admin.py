from django.contrib import admin
from .models import Usuario, Publicacao, ContadorView

admin.site.register(Usuario)
admin.site.register(Publicacao)
admin.site.register(ContadorView)
