from django.shortcuts import render, redirect
from django.db.models import Q, Count
from .models import League, Team, Player

from . import team_maker


def index(request):
    context = {
        "leagues": League.objects.all(),
        # ... todas las ligas de béisbol
        "leaguesBaseball": League.objects.filter(name__contains="baseball"),
        # ... todas las ligas de mujeres
        "leaguesWomens": League.objects.filter(name__contains="women"),
        # ... todas las ligas donde el deporte es cualquier tipo de hockey
        "leaguesHockey": League.objects.filter(name__contains="hocke"),
        # ... todas las ligas donde el deporte no sea football
        "leaguesExclFootball": League.objects.exclude(Q(name__contains="footb") | Q(name__contains="Soccer")),
        # ... todas las ligas que se llaman "conferencias"
        "leaguesConference": League.objects.filter(name__contains="conferen"),
        # ... todas las ligas de la región atlántica
        "leaguesAtlantic": League.objects.filter(name__contains="atlantic"),
        # ... todos los equipos con sede en Dallas
        "locationDallas": Team.objects.filter(location__contains="dallas"),
        # ... todos los equipos nombraron los Raptors
        "raptorTeams": Team.objects.filter(team_name__contains="rapt"),
        # ... todos los equipos cuya ubicación incluye "Ciudad"
        "locationCity": Team.objects.filter(location__contains="city"),
        # ... todos los equipos cuyos nombres comienzan con "T"
        "startWithT": Team.objects.filter(team_name__startswith="T"),
        # ... todos los equipos, ordenados alfabéticamente por ubicación
        "orderLocation": Team.objects.all().order_by("location"),
        # ... todos los equipos, ordenados por nombre de equipo en orden alfabético inverso
        "orderinvTeam": Team.objects.all().order_by("-team_name"),
        # ... cada jugador con apellido "Cooper"
        "lstnameCooper": Player.objects.filter(last_name="Cooper"),
        # ... cada jugador con nombre "Joshua"
        "frsnameJoshua": Player.objects.filter(first_name="Joshua"),
        # ... todos los jugadores con el apellido "Cooper" EXCEPTO aquellos con "Joshua" como primer nombre
        "cooperExclJoshua": Player.objects.filter(last_name="Cooper").exclude(first_name="Joshua"),
        # ... todos los jugadores con nombre "Alexander" O nombre "Wyatt"
        "alexORwya": Player.objects.filter(Q(first_name="Alexander") | Q(first_name="Wyatt")).order_by('first_name', "last_name"),
        #########################################################################################################################
        #########################################################################################################################
        "teams": Team.objects.all(),
        "players": Player.objects.all(),
        # ... todos los equipos en la Atlantic Soccer Conference
        "teamsAtlanticSoccer": Team.objects.all().filter(league__name="Atlantic Soccer Conference"),
        # ... todos los jugadores(actuales) en los Boston Penguins
        "playersPenguins": Player.objects.all().filter(curr_team__location="Boston", curr_team__team_name="Penguins"),
        # ... todos los jugadores(actuales) en la International Collegiate Baseball Conference
        "playersIntColBasCon": Player.objects.all().filter(curr_team__league__name="International Collegiate Baseball Conference").order_by('id'),
        # ... todos los jugadores(actuales) en la Conferencia Americana de Fútbol Amateur con el apellido "López"
        "playerLopez": Player.objects.all().filter(curr_team__league__name="American Conference of Amateur Football", last_name="Lopez"),
        # ... todos los jugadores de fútbol
        "playerFootball": Player.objects.distinct().filter(Q(all_teams__league__sport="Football") | Q(all_teams__league__sport="Soccer")).order_by('id'),
        # ... todos los equipos con un jugador(actual) llamado "Sophia"
        "teamSophia": Team.objects.all().filter(curr_players__first_name="Sophia").order_by('id'),
        # ... todas las ligas con un jugador(actual) llamado "Sophia"
        "leagueSophia": League.objects.all().filter(teams__curr_players__first_name="Sophia").order_by('id'),
        # ... todos con el apellido "Flores" que NO(actualmente) juegan para los Washington Roughriders
        "playerFlores": Player.objects.all().filter(last_name="Flores").exclude(Q(curr_team__location="Washington") & Q(curr_team__team_name="Roughriders")),
        # ... todos los equipos, pasados y presentes, con los que Samuel Evans ha jugado
        "teamsamuel": Team.objects.all().filter(Q(all_players__first_name="Samuel") & Q(all_players__last_name="Evans")).order_by('id'),
        # ... todos los jugadores, pasados y presentes, con los gatos tigre de Manitoba
        "playersManitoba": Player.objects.all().filter(Q(all_teams__location="Manitoba") & Q(all_teams__team_name="Tiger-Cats")).order_by('id'),
        # ... todos los jugadores que anteriormente estaban(pero que no lo están) con los Wichita Vikings
        "playerswichita": Player.objects.all().filter(Q(all_teams__location="Wichita") & Q(all_teams__team_name="Vikings")).exclude(Q(curr_team__location="Wichita") & Q(curr_team__team_name="Vikings")).order_by('id'),
        # ... cada equipo para el que Jacob Gray jugó antes de unirse a los Oregon Colts
        "teamJacob": Team.objects.all().filter(Q(all_players__last_name="Gray") & Q(all_players__first_name="Jacob")).exclude(location="Oregon", team_name="Colts").order_by('id'),
        # ... todos llamados "Joshua" que alguna vez han jugado en la Federación Atlántica de Jugadores de Béisbol Amateur
        "playersJoshua": Player.objects.all().filter(all_teams__league__name="Atlantic Federation of Amateur Baseball Players", first_name='Joshua').exclude(curr_team__league__name="Atlantic Federation of Amateur Baseball Players"),
        # ... todos los equipos que han tenido 12 o más jugadores, pasados y presentes. (SUGERENCIA: busque la función de anotación de Django).
        "teamsgteTwelve": Team.objects.all().annotate(cantidad=Count("all_players")).filter(cantidad__gte=12).order_by('cantidad'),
        # ... todos los jugadores y el número de equipos para los que jugó, ordenados por la cantidad de equipos para los que han jugado
        "playersAndTeams": Player.objects.annotate(cantidad=Count("all_teams")).order_by("-cantidad"),

    }
    return render(request, "leagues/index.html", context)


def make_data(request):
    team_maker.gen_leagues(10)
    team_maker.gen_teams(50)
    team_maker.gen_players(200)

    return redirect("index")
