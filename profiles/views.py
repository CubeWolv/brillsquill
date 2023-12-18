from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate ,login as dj_login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignupForm, PoemForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile,Poems,ImagePoem
from itertools import chain




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

    return render(request, './profiles/join/login.html', {'page': page})


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

    return render(request, 'profiles/join/signup.html', {'form': form})


from django.utils import timezone
from operator import attrgetter
@login_required
def profiles(request, username):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(person=user)

    poems = Poems.objects.filter(author=user)
    image_poems = ImagePoem.objects.filter(author=user)

    # Combine the two querysets and sort them by created_on timestamp
    combined_poems = sorted(
        chain(poems, image_poems),
        key=attrgetter('created_on'),
        reverse=True
    )

    poem_form = PoemForm(request.POST or None)

    if request.method == 'POST':
        if 'poem_submit' in request.POST:
            if poem_form.is_valid():
                poem_form.save(user=user_profile.person)
                return redirect('profile', username=user.username)
        elif 'image_poem_submit' in request.POST:
            title = request.POST.get('title')
            image = request.FILES.get('image')
            if title and image:
                image_poem = ImagePoem.objects.create(author=user, title=title, image=image, created_on=timezone.now())
                return redirect('profile', username=user.username)

    context = {
        'username': username,
        'poem_form': poem_form,
        'combined_poems': combined_poems,
        'user_profile': user_profile,  # Add user_profile to the context
    }

    return render(request, 'profiles/profiles/profile.html', context)

@login_required
def delete_poem(request, username, poem_id):
    user = request.user

    # Ensure that the poem belongs to the logged-in user
    poem = get_object_or_404(Poems, id=poem_id, author=user)

    # Delete the poem
    poem.delete()
    messages.success(request, 'Poem deleted.') 

    return redirect('profile', username=username)



@login_required
def delete_image_poem(request, username, image_poem_id):
    user = request.user

    # Ensure that the image poem belongs to the logged-in user
    image_poem = get_object_or_404(ImagePoem, id=image_poem_id, author=user)

    # Delete the image poem
    image_poem.delete()
    messages.success(request, 'Image Poem deleted.')

    # Redirect to the profile page after deleting the image poem
    return redirect('profile', username=username)



@login_required
def edit_poem(request, username, poem_id):
    user = request.user
    poem = get_object_or_404(Poems, id=poem_id, author=user)

    if request.method == 'POST':
        poem_form = PoemForm(request.POST, instance=poem)
        if poem_form.is_valid():
            poem_form.save()
            messages.success(request, 'Poem edited successfully.')  # Add success message
            return redirect('profile', username=username)
    else:
        poem_form = PoemForm(instance=poem)

    context = {
        'username': username,
        'poem': poem,
        'action': 'edit',
        'poem_form': poem_form,
    }
    return render(request, 'profiles/poem/editpoem.html', context)




@login_required
def edit_image_poem(request, username, image_poem_id):
    user = request.user
    image_poem = get_object_or_404(ImagePoem, id=image_poem_id, author=user)

    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')

        # Update the image poem fields
        image_poem.title = title
        if image:
            image_poem.image = image

        image_poem.save()
        messages.success(request, 'Image Poem edited successfully.')  # Add success message
        return redirect('profile', username=username)
    else:
        # Populate the form with existing data
        title = image_poem.title

    context = {
        'username': username,
        'image_poem': image_poem,
        'action': 'edit',
        'title': title,
        # Add any other necessary data for your template
    }
    return render(request, 'profiles/poem/editimagepoem.html', context)




def share(request, poem_id):
    poem = None
    image_poem = None
    user_profile = None

    try:
        # Try to get a Poem with the given ID
        poem = get_object_or_404(Poems, id=poem_id)
        user_profile = get_object_or_404(UserProfile, person=poem.author)
    except:
        try:
            # If not a Poem, try to get an ImagePoem with the given ID
            image_poem = get_object_or_404(ImagePoem, id=poem_id)
            user_profile = get_object_or_404(UserProfile, person=image_poem.author)
        except:
            pass  # Handle the case when neither Poem nor ImagePoem is found

    context = {'poem': poem, 'image_poem': image_poem, 'user_profile': user_profile}
    return render(request, 'profiles/poem/share.html', context)

@login_required
def accountcenter(request, username):
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(person=user)

    if request.method == 'POST':
        # Handle form submission and update the UserProfile
        user.username = request.POST.get('username')
        profile.country = request.POST.get('country')

        # Handle image upload
        if 'image' in request.FILES:
            profile.image = request.FILES['image']

        # Add more fields as needed

        user.save()
        profile.save()
        return redirect('accountcenter', username=username)

    context ={
        'username': username,
        'profile': profile,
    }
    return render(request ,'profiles/accountcenter/accountcenter.html', context)






def logout_view(request):
    logout(request)
    return redirect('home')