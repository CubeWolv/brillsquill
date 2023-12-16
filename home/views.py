from django.shortcuts import render
from profiles.models import Poems ,UserProfile # Make sure to import your Poem model

def home(request):
    poems = Poems.objects.all()
    user_profiles = UserProfile.objects.all()
    return render(request, 'home/home.html', {'poems': poems, 'user_profiles': user_profiles})
