from django.contrib import admin
from .models import Game, Result, Ranking, User

# Register your models here.
admin.site.register(Game)
admin.site.register(Result)
admin.site.register(Ranking)
admin.site.register(User)