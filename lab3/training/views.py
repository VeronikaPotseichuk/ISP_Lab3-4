from django.shortcuts import render


def index(request):
    return render(request, 'training/start.html')

def about(request):
    return render(request, 'training/about.html')