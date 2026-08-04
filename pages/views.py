from django.shortcuts import render, redirect


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'landing.html')

def recursos(request):
    if not request.user.is_authenticated:
        return redirect('landing')
    
    return render(request, 'recursos.html')

def avaliacoes(request):
    if not request.user.is_authenticated:
        return redirect('landing')
    
    return render(request, 'avaliacoes.html')

def clubes(request):
    if not request.user.is_authenticated:
        return redirect('landing')
    
    return render(request, 'clubes.html')

def sobre(request):
    if not request.user.is_authenticated:
        return redirect('landing')
    
    return render(request, 'sobre.html')