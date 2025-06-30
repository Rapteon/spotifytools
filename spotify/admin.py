from django.contrib import admin

# Register your models here.
from .models import Credential, Token, SpotifyUser

admin.site.register(Credential)
admin.site.register(Token)
admin.site.register(SpotifyUser)
