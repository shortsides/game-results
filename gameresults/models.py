from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def serialize(self):
        return {
            "label": self.username,
            "value": str(self.id)
        }

class Game(models.Model):
    game_title = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.game_title}"

class Result(models.Model):
    winner = models.ManyToManyField('User', blank=False, related_name='games_won')
    players = models.ManyToManyField('User', blank=False, related_name='games_played')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, blank=False, related_name='results')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        winners = self.winner.all()
        winner_names = []
        for winner in winners:
            winner_names.append(winner.username)
        winner_names = str(winner_names).replace("'","")
        winner_names = str(winner_names).strip("[]")
        winner_names = str(winner_names).replace(","," &")
        return f'{winner_names} won {self.game}'

class Ranking(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rankings')
    game = models.ForeignKey('Game', blank=True, null=True, on_delete=models.CASCADE, related_name='rankings')
    result = models.ForeignKey('Result', on_delete=models.CASCADE, related_name='rankings')
    mu = models.FloatField(default=25.0)
    sigma = models.FloatField(default=25. / 3.)
    rank = models.FloatField(default=25.0)

    def __str__(self):
        return f"{self.user} score is {round(self.rank, 2)} in {self.game} for the result {self.result}"