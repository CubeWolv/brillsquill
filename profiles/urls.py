from django.urls import path

from . import views

urlpatterns = [
    path('signup' , views.signup, name='signup'),
    path('login' , views.login, name='login'),
    path('profile/<str:username>/',views.profiles, name="profile")
]