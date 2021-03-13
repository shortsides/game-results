from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addgame", views.addgame, name="addgame"),
    path("addresult", views.addresult, name="addresult"),
    path("rankings", views.rankings_page, name="rankings"),
    path("rankings/<game>", views.game_rankings, name="game_rankings"),
    path("games", views.games, name="games"),
    path("change_password", views.change_password, name="change_password"),

    # API Routes
    path("players", views.players, name="players")
]
