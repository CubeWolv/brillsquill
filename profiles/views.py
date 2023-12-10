from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login as dj_login
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignupForm

# Create your views here.



def login(request):
    page = 'login'

    # Check if the user is already logged in
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            dj_login(request, user)
            return redirect('profile')

        else:
            messages.info(request, 'Invalid username or password')
            return redirect("login")

    if 'next' in request.POST:
        return redirect(request.POST['next'])

    return render(request, './profiles/login.html', {'page': page})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Log in the user
            user = authenticate(username=username, password=password)
            dj_login(request, user)

            return redirect('home')  # Replace 'home' with your home page URL
    else:
        form = SignupForm()

    return render(request, 'profiles/signup.html', {'form': form})

