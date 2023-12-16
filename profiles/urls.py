from django.urls import path

from . import views

urlpatterns = [
    path('signup' , views.signup, name='signup'),
    path('login' , views.login, name='login'),
    path('profile/<str:username>/',views.profiles, name="profile"),
    path('<str:username>/delete_poem/<int:poem_id>/', views.delete_poem, name='delete_poem'),
    path('<str:username>/edit_poem/<int:poem_id>/', views.edit_poem, name='edit_poem'),
    path('<int:poem_id>/share/' ,views.share, name='share'),
    path('accountcenter/<str:username>' ,views.accountcenter ,name='accountcenter'),
    path('logout/', views.logout_view, name='logout'),


]