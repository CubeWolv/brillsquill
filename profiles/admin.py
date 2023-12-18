from django.contrib import admin
from .models import UserProfile ,Poems,ImagePoem

admin.site.register(UserProfile)
class CampaignAdmin(admin.ModelAdmin):
    list_display =("country","person")

@admin.register(Poems)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('author' ,'title', 'created_on')

@admin.register(ImagePoem)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title','created_on')