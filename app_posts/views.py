from django.shortcuts import render, redirect
from app_posts.models import Publicacao, Usuario, ContadorView

def GetTopPosts():
    posts = list(Publicacao.objects.filter(status="3"))
    posts.sort(key=lambda x: x.GetViews(), reverse=True)
    return posts[:3]


def GetTopJogos():
    jogos = list(Publicacao.objects.filter(tipo = "1",status="3"))
    jogos.sort(key=lambda x: x.GetViews(), reverse=True)
    return jogos[:3]


def Home(request):
    return render(request, 'home.html', {
        "title":"Home",
        "navActive":"Sobre",
        "posts": GetTopPosts(),
        "jogos": GetTopJogos(),
        "equipe": Usuario.objects.filter(classe = "2")
    })


def Publicacoes(request):
    return render(request, 'Publicacoes.html', {
        "title":"Publicações",
        "navActive":"Publicacoes",
        "posts":list(Publicacao.objects.filter(status="3"))
    })


def Jogos(request):
    return render(request, 'Jogos.html', {
        "title":"Jogos",
        "navActive":"Jogos",
        "jogos":Publicacao.objects.filter(tipo = "1")
    })


def Perfil(request, user):
    if Usuario.objects.filter(username = user):
        usu = Usuario.objects.get(username = user)
        edicao = False
        if request.user.is_authenticated:
            if usu.username == request.user.username:
                edicao = True
        return render(request, 'Perfil.html', {
            "title":usu.username,
            "navActive":"Perfil",
            "usuario":usu,
            "edicao": edicao,
            "myposts":usu.GetPosts()
        })
    else:
        return render(request, 'Erro.html', {
            "title":"ERROR",
            "navActive":"ERRO",
            "msg":"'Usuário não encontrado!'"
        })


def Post(request, uid):
    if Publicacao.objects.filter(UID = uid):
        post = Publicacao.objects.get(UID = uid)
        if ContadorView.objects.filter(publicacao = post):
            cont = ContadorView.objects.get(publicacao = post)
            cont.qtd += 1
            cont.save()
        else:
            cont = ContadorView()
            cont.publicacao = post
            cont.qtd = 1
            cont.save()
        edicao = False
        if request.user.is_authenticated:
            user = Usuario.objects.get(username = request.user.username)
            if user == post.autor:
                edicao = True
        return render(request, 'Post.html', {
            "title":post.titulo,
            "navActive":"Publicacoes",
            "edicao":edicao,
            "post":post,
        })
    else:
        return render(request, 'Erro.html', {
            "title":"ERROR",
            "navActive":"ERRO",
            "msg":"'Publicação não encontrada!'"
        })


def EditarPost(request, uid):
    if request.user.is_authenticated:
        user = Usuario.objects.get(username = request.user.username)
        if Publicacao.objects.filter(UID = uid) and request.method == "GET":
            post = Publicacao.objects.get(UID = uid)
            if post.autor == user:
                return render(request, 'EdicaoPost.html', {
                    "title":"Edição",
                    "navActive":"Publicacoes",
                    "post":post,
                })
            else:
                return render(request, 'Erro.html', {
                    "title":"ERROR",
                    "navActive":"ERRO",
                    "msg":"'Você não tem acesso a edição dessa pagina!'"
                })
        elif Publicacao.objects.filter(UID = uid) and request.method == "POST":
            post = Publicacao.objects.get(UID = uid)
            post.titulo = request.POST["titulo"]
            post.resumo = request.POST["resumo"]
            post.conteudo = request.POST["conteudo"]
            post.save()
            return redirect("Post",post.UID)
        else:
            return render(request, 'Erro.html', {
                "title":"ERROR",
                "navActive":"ERRO",
                "msg":"'Publicação não encontrada!'"
            })


def NovoPost(request):
    if request.user.is_authenticated:
        user = Usuario.objects.get(username = request.user.username)
        if request.method == "GET":
            return render(request, 'NovoPost.html', {
                "title":"Novo Post",
                "navActive":"Publicacoes",
            })
        elif request.method == "POST":
            post = Publicacao()
            post.titulo = request.POST["titulo"]
            post.resumo = request.POST["resumo"]
            post.conteudo = request.POST["conteudo"]
            post.autor = user
            post.save()
            return redirect("Post",post.UID)