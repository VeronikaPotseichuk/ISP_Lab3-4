from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login
from training.forms import UserCreationForm

def index(request):
    return render(request, 'training/start.html')

def about(request):
    return render(request, 'training/about.html')

class Sign_up(View):

    def get(self, request):
        context = {
            'form':  UserCreationForm()
        }
        return render(request, 'registration/sign_up.html', context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')        
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home-page')
        context = {
            'form': form
        }
        return render(request, 'registration/sign_up.html', context)
