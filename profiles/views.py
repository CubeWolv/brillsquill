from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate ,login as dj_login
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignupForm, UserProfileForm,PoemForm
from .models import UserProfile,Poems


# Create your views here.



def login(request):
    page = 'login'

    # Check if the user is already logged in
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            dj_login(request, user)
            return redirect('home')

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

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return render(request, 'profiles/signup.html', {'form': form})

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Log in the user
            user = authenticate(username=username, password=password)
            dj_login(request, user)

            return redirect('home')  # Replace 'home' with your home page URL
    else:
        form = SignupForm()

    return render(request, 'profiles/signup.html', {'form': form})


from django.contrib.auth.decorators import login_required

@login_required
def profiles(request, username):
    # Assuming you have imported necessary modules and classes

    user = request.user  # Get the currently authenticated user
    user_profile, created = UserProfile.objects.get_or_create(person=user)

    poem_form = PoemForm(request.POST or None)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Update the profile with the new data
            form.save()

            # Handle poem form submission
            if poem_form.is_valid():
                poem_form.save(user=user_profile.person)

            return redirect('profile', username=user.username)
    else:
        form = UserProfileForm(instance=user_profile)

    # Fetch poems for the logged-in user
    poems = Poems.objects.filter(author=user)

    context = {
        'username': username,
        'form': form,
        'user_profile': user_profile,
        'poem_form': poem_form,
        'poems': poems,
    }
    return render(request, 'profiles/profile.html', context)
