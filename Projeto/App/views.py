from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


def cadastro(request):
    erro = ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not username or not email or not password:
            erro = 'Preencha todos os campos.'
        elif User.objects.filter(username=username).exists():
            erro = 'Esse nome de usuário já está em uso.'
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('login')

    return render(request, 'cadastro.html', {'erro': erro})

def entrar(request):
    erro = ''

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)
            return redirect('home')

        erro = 'Nome de usuário ou senha incorretos.'

    return render(request, 'login.html', {'erro': erro})
@require_POST
def sair(request):
    logout(request)
    return redirect('login')