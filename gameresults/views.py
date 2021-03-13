import json

from datetime import timedelta, datetime

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .helpers import calculate_rankings
from .models import User, Game, Result, Ranking

class CreateGame(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['game_title']
        widgets = {'game_title': forms.TextInput(attrs={'class': 'game-select'})}

class CreateResult(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['game']
        widgets = {'game': forms.Select(attrs={'class': 'game-select'})}
    
    # override default select option to '' instead of '-------'
    def __init__(self, *args, **kwargs):
        super(CreateResult, self).__init__(*args, **kwargs)
        self.fields['game'].empty_label = ''


def index(request):

    results = Result.objects.all().order_by('-timestamp')[:10]
    
    for result in results:
        result.timestamp = result.timestamp + timedelta(0, 0, 0, 0, 0, 11)
        result.timestamp = result.timestamp.strftime("%a %d %b, %H:%M %p")

    return render(request, "gameresults/index.html", {
        "addresult": CreateResult(),
        "games": Game.objects.all().order_by('game_title'),
        "results": results
    })


def rankings_page(request):
    players = User.objects.all()
    calculate_rankings(game='')
    rankings = []

    # get most recent overall rank score for each player
    for player in players:
        past_2_rankings = Ranking.objects.filter(game__isnull=True, user=player).order_by('-result__timestamp')[:2]
        try:
            current_ranking = past_2_rankings[0]
            current_ranking.change = current_ranking.rank - past_2_rankings[1].rank
            rankings.append(current_ranking)
        except:
            pass

    # sort results by highest rank
    rankings = sorted(rankings, key=lambda ranking: ranking.rank, reverse=True)

    return render(request, "gameresults/rankings.html", {
        "games": Game.objects.all().order_by('game_title'),
        "ratings": rankings
    })


def game_rankings(request, game):
    game = Game.objects.get(game_title=game)
    players = User.objects.all()

    rankings = []

    # get most recent rank score for each player for this game
    for player in players:
        past_2_rankings = Ranking.objects.filter(game=game, user=player).order_by('-result__timestamp')[:2]
        try:
            current_ranking = past_2_rankings[0]
            current_ranking.change = current_ranking.rank - past_2_rankings[1].rank
            rankings.append(current_ranking)
        except:
            pass
    
    # sort results by highest rank
    rankings = sorted(rankings, key=lambda ranking: ranking.rank, reverse=True)
    
    return render(request, "gameresults/rankings.html", {
        "game": game,
        "games": Game.objects.all().order_by('game_title'),
        "ratings": rankings
    })


def games(request):

    return render(request, "gameresults/games.html", {
        "addgame": CreateGame(),
        "addresult": CreateResult(),
        "games": Game.objects.all().order_by('game_title')
    })


def addgame(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreateGame(request.POST)
            if form.is_valid():
            # Attempt to create game
                title = form['game_title'].value()
                games = Game.objects.filter(game_title__iexact=title)
                if not games.exists():
                    game = form.save(commit=False)
                    game.save()
                    return render(request, "gameresults/games.html", {
                        "message": f"{title} added successfully.",
                        "addgame": CreateGame(),
                        "addresult": CreateResult(),
                        "games": Game.objects.all().order_by('game_title')
                    })
                else:
                    return render(request, "gameresults/games.html", {
                        "message": "Game already exists.",
                        "addgame": CreateGame(),
                        "addresult": CreateResult(),
                        "games": Game.objects.all().order_by('game_title')
                    })

                return redirect(reverse("games"))
    else:
        messages.info(request, "You must log in to add a new game.")
        return redirect('games')


@login_required
@csrf_exempt
def addresult(request):
    if request.method == "POST":
        data = json.loads(request.body)
        game = Game.objects.get(id=data["game"])
        players = []
        winner = []
        for i in data["players"]:
            players.append(User.objects.get(id=i))
        for j in data["winner"]:
            winner.append(User.objects.get(id=j))

        instance = Result.objects.create(game=game)
        instance.players.set(players)
        instance.winner.set(winner)
        calculate_rankings(game=game)
        messages.info(request, "Result added successfully")
        return JsonResponse({})


@csrf_exempt
def players(request):
    players = User.objects.filter(is_staff=False)

    return JsonResponse([player.serialize() for player in players], safe=False)


@login_required
def change_password(request):
    
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "gameresults/change_password.html", {
        "form": form
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "gameresults/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "gameresults/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "gameresults/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "gameresults/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "gameresults/register.html")
