from datetime import date
from django.db import models
from django.contrib.auth.models import User

def MakeUID(titulo):
    ajustado = titulo.replace("á","a")
    return ajustado.replace(" ","-")


class Usuario(User):
    classes = (
        ("0","Autor"),
        ("1","Editor"),
        ("2","Gerente"),
    )
    classe = models.CharField("Classe do Usuario",max_length=20, choices=classes, null=True, blank=True)
    biografia = models.TextField("Biografia do Usuario",max_length=2000, null=True, blank=True)
    image = models.CharField("Imagem de perfil do Usuario",max_length=10000, null=True, blank=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username

    def GetPosts(self):
        return list(Publicacao.objects.filter(autor=self))

    def getQtdPublicacoes(self):
        return len(list(Publicacao.objects.filter(autor=self)))


class Publicacao(models.Model):
    UID = models.CharField("Código UID da publicação", max_length=200, null=True, blank=True)
    titulo = models.CharField("Título da publicação", max_length=150)
    resumo = models.TextField("Resumo da publicação", max_length=500, null=True, blank=True)
    conteudo = models.TextField("Conteúdo [ HTML + Bootstrap ]", max_length=50000, null=True, blank=True)
    autor = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    image = models.CharField("Imagem de perfil do Usuario",max_length=10000, null=True, blank=True)
    data_publicacao = models.DateField("Data de Publicação", null=True, blank=True)

    tipos = (
        ("0","POST"),
        ("1","JOGO"),
    )
    tipo = models.CharField("Tipo da Publicação", max_length=5, choices=tipos, null = True, blank = True, default=tipos[0])
    estados = (
        ("0","salvo"),
        ("1","revisão"),
        ("2","revisado"),
        ("3","publicado"),
    )
    status = models.CharField("Status da Publicação", max_length=15, choices=estados, null = True, blank = True, default=estados[0])

    class Meta:
        verbose_name = "Publicação"
        verbose_name_plural = "Publicações"
    
    def __str__(self):
        return str(self.UID) + " | " + self.titulo

    def save(self, *args, **kwargs):
        self.UID = MakeUID(self.titulo)
        super().save(*args, **kwargs)

    def Publicar(self):
        self.data_publicacao = date.now()
        self.status = self.estados[3]
        self.save()

    def getStatus(self):
        return self.estados[int(self.status)][1]


    def GetViews(self):
        if ContadorView.objects.filter(publicacao=self):
            return ContadorView.objects.get(publicacao=self).qtd
        else:
            cont = ContadorView()
            cont.publicacao = self
            cont.qtd = 0
            cont.save()
            return 0


class ContadorView(models.Model):
    qtd = models.IntegerField("Quantidade de views",default=0)
    publicacao = models.ForeignKey(Publicacao,on_delete=models.CASCADE)

    def __str__(self):
        return "{} views na publicação: {}".format(self.qtd, self.titulo)
