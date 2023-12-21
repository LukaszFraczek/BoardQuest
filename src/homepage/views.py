from django.shortcuts import render


def home(request):
    return render(request, 'homepage/home.html')


def handling_404(request, exception):
    return render(request, '404.html', {})
