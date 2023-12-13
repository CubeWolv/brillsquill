from django.shortcuts import render
from profiles.models import Poems  # Make sure to import your Poem model

def home(request):
    poems = Poems.objects.all()
    return render(request, 'home/home.html', {'poems': poems})