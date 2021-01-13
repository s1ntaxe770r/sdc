from django.shortcuts import render
from django.contrib.auth import login, authenticate
from . import forms
# Create your views here.
def index(parameter_list):
    """
    docstring
    """
    pass

def signup(request):
    if request.method == 'POST':
        form  = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
    else:
        form =  forms.RegisterForm()
        
    return render(request, 'signup.html', {'form': form})    