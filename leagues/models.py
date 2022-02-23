from django.db import models


class League(models.Model):
    name = models.CharField(max_length=50)
    sport = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # teams=lista de equipos de la liga

    def __str__(self):
        return f"{self.name} {self.sport} {self.id}"


class Team(models.Model):
    location = models.CharField(max_length=50)
    team_name = models.CharField(max_length=50)
    league = models.ForeignKey(
        League, related_name="teams", on_delete=models.CASCADE)
    # curr_players=lista de jugadores actuales en el equipo
    # all_players=lista de jugadores totales en el equipo


def __str__(self):
    return f"{self.location} {self.team_name} {self.league}"


class Player(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    curr_team = models.ForeignKey(
        Team, related_name="curr_players", on_delete=models.CASCADE)
    all_teams = models.ManyToManyField(Team, related_name="all_players")
