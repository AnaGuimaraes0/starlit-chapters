from django.shortcuts import render, redirect


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'landing.html')

def recursos(request):
    return render(request, 'recursos.html')

def avaliacoes(request):
    return render(request, 'avaliacoes.html')

def clubes(request):
    return render(request, 'clubes.html')

def sobre(request):
    return render(request, 'sobre.html')