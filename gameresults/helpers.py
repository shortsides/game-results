from django.db import transaction
from .models import User, Game, Result, Ranking

from trueskill import Rating, quality, rate

def calculate_rankings(game=""):
    players = {p.pk: p for p in User.objects.all()}
    ratings = {pk: (Rating(),) for pk in players}
    if game:
        results = Result.objects.filter(game=game)
    else:
        results = Result.objects.all()
    rankings = []

    for result in results:
        player_ids = [p.pk for p in result.players.all()]
        rating_groups = [ratings[id] for id in player_ids]
        winners = [p.pk for p in result.winner.all()]
        ranks = [id not in winners for id in player_ids]
        new_ratings = rate(rating_groups, ranks=ranks)
        
        for i in range(len(player_ids)):
            ranking = Ranking()
            rating = new_ratings[i]
            ratings[player_ids[i]] = rating
            ranking.result = result
            ranking.user = players[player_ids[i]]
            ranking.mu = rating[0].mu
            ranking.sigma = rating[0].sigma
            ranking.rank = rating[0].mu - 3 * rating[0].sigma
            if game:
                ranking.game = result.game
            rankings.append(ranking)

    with transaction.atomic():
        if game:
            Ranking.objects.filter(game=game).delete()
        else:
            Ranking.objects.filter(game__isnull=True).delete()
        Ranking.objects.bulk_create(rankings)
        """
        for pk, player in players.items():
            rating = ratings[pk]
            player.mu = rating[0].mu
            player.sigma = rating[0].sigma
            player.rank = rating[0].mu - 3 * rating[0].sigma
            player.save()
        """
