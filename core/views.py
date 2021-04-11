from django.http import HttpRequest
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Team, Contest, Attempt
from .serializers import TeamSerializer, ContestSerializer, \
    ActiveContestAttemptSerializer, ArchiveContestAttemptSerializer, \
    NewAttemptSerializer, UserSerializer
from contest_platform.settings import MAX_TEAM_MEMBERS


def active_contests() -> QuerySet:
    """Returns QuerySet of active contests."""
    now = timezone.now()
    return Contest.objects.filter(ends_at__gt=now, starts_at__lte=now).order_by('-ends_at')


def archive_contests() -> QuerySet:
    """Returns QuerySet of archive contests."""
    return Contest.objects.filter(ends_at__lte=timezone.now()).order_by('-ends_at')


def future_contests() -> QuerySet:
    """Returns QuerySet of future contest."""
    return Contest.objects.filter(starts_at__gt=timezone.now()).order_by('-starts_at')


@api_view(['GET'])
def contests(request: HttpRequest, contests_type: str = 'all', contest_id: int = None) -> Response:
    """Main contest view, returns json dictionary with requested contests or 404."""
    contests_types = {'all': lambda: Contest.objects.all(),
                      'active': active_contests,
                      'archive': archive_contests,
                      'future': future_contests,
                      'my': active_contests}
    if contest_id is not None:
        contest = Contest.objects.filter(pk=contest_id).first()
        if contest is None:
            return Response({'message': 'no such contest'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ContestSerializer(contest).data)
    if contests_type not in contests_types:
        return Response({'message': 'no such contest type'}, status=status.HTTP_404_NOT_FOUND)
    contests_query = contests_types[contests_type]()
    if contests_type == 'my' and request.user.is_authenticated:
        contests_query = contests_query.filter(team__in=request.user.team_set.all())
    serialized = ContestSerializer(contests_query, many=True)
    return Response(serialized.data)


@login_required
@api_view(['GET', 'POST'])
def attempts(request: HttpRequest, contest_id: int = None) -> Response:
    """
    Returns list of attempts if request method is GET,
    or creates new attempt if request method is post.
    """
    if request.method == 'GET':
        serializer = ActiveContestAttemptSerializer
        attempts_query = Attempt.objects.filter(team__in=request.user.team_set.all())
        if contest_id is not None:
            attempts_query = attempts_query.filter(team__contest_id=contest_id)
            try:
                if Contest.objects.get(pk=contest_id).ends_at <= timezone.now():
                    serializer = ArchiveContestAttemptSerializer
            except Exception:
                return Response(status=status.HTTP_404_NOT_FOUND)
        serialized = serializer(attempts_query, many=True, context={'request': request})
        return Response(serialized.data)

    if request.method == 'POST':
        if contest_id is None:
            return Response({'message': 'contest_id is missing'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            contest = Contest.objects.get(pk=contest_id)
        except Exception:
            return Response({'message': 'no such contest'}, status=status.HTTP_404_NOT_FOUND)

        if contest.starts_at > timezone.now() or contest.ends_at < timezone.now():
            return Response({'message': 'you can\'t create attempt in inactive contest'},
                            status=status.HTTP_403_FORBIDDEN)

        data = {'team_id': request.user.team_set.get(contest=contest).pk,
                'file': request.FILES.get('file')}
        serialized = NewAttemptSerializer(data=data)
        if serialized.is_valid():
            instance = serialized.save()
            instance.save()
            return Response({'message': 'Attempt created successfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PATCH'])
def teams(request: HttpRequest, contest_id: int = None, team_id: int = None) -> Response:
    """
    Returns list of teams registered on contest if its id is given,
    else returns user teams or all teams depends on if user is authenticated.
    If contest_id is given, supports GET parameter "order_by",
    possible values: "public_score" and "private_score".
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'message': 'you must be authenticated to create teams'},
                            status=status.HTTP_403_FORBIDDEN)
        data = dict(request.data)
        data['contest'] = contest_id
        data['name'] = data['name'][0]
        serialized = TeamSerializer(data=data)
        if serialized.is_valid():
            team = serialized.save()
            team.users.add(request.user)
            return Response({'message': 'Team successfully created'},
                            status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        if not request.user.is_authenticated:
            return Response({'message': 'you must be authenticated to join teams'},
                            status=status.HTTP_403_FORBIDDEN)
        team = Team.objects.filter(pk=team_id).first()
        if team is None:
            return Response({'message': 'no such team'}, status=status.HTTP_404_NOT_FOUND)
        if len(team.users.all()) == MAX_TEAM_MEMBERS:
            return Response({'message': 'team has maximum number of members'},
                            status=status.HTTP_403_FORBIDDEN)
        if request.user.team_set.filter(contest_id=team.contest_id).first() is not None:
            return Response({'message': 'you have already registered on this contest'},
                            status=status.HTTP_403_FORBIDDEN)
        team.users.add(request.user)
        team.save()
        return Response({'message': 'Successfully joined the team'})

    if team_id is not None:
        team = Team.objects.filter(pk=team_id).first()
        if team is None:
            return Response({'message': 'no such team'}, status=status.HTTP_404_NOT_FOUND)
        return Response(TeamSerializer(team).data)
    if contest_id is None:
        if request.user.is_authenticated:
            teams_query = request.user.team_set.all()
        else:
            teams_query = Team.objects.all()
        contest = None
    else:
        contest = Contest.objects.filter(pk=contest_id).first()
        if contest is None:
            return Response({'message': 'no such contest'},
                            status=status.HTTP_404_NOT_FOUND)

        teams_query = Team.objects.filter(contest=contest)
    order = request.GET.get('order_by')
    if order == 'private_score':
        if contest_id is None or not contest.ends_at < timezone.now():
            return Response(
                {'message': 'private leaderboard is closed while contest isn\'t ended'},
                status=status.HTTP_403_FORBIDDEN
            )
        score = models.Max('attempt__private_score')
    else:
        score = models.Max('attempt__public_score')
    teams_query = teams_query.annotate(score=score)
    if str(order).endswith('score'):
        teams_query = teams_query.order_by('-score')

    serialized = TeamSerializer(teams_query, many=True, context={'request': request})
    return Response(serialized.data)


@api_view(['GET'])
def get_permissions(request: HttpRequest, contest_id: int) -> Response:
    permissions = {'register': False, 'submit': False, 'get_attempts': False}
    contest = Contest.objects.filter(pk=contest_id).first()
    if contest is None:
        return Response({'message': 'no such contest'}, status=status.HTTP_404_NOT_FOUND)
    team = request.user.team_set.filter(contest_id=contest_id).first()
    is_registered = request.user.is_authenticated and team is not None
    if is_registered and Attempt.objects.filter(team=team).first() is not None:
        permissions['get_attempts'] = True
    now = timezone.now()
    if now < contest.ends_at:
        if is_registered and contest.starts_at < now:
            permissions['submit'] = True
        else:
            permissions['register'] = True
    return Response(permissions)


@api_view(['POST'])
def register_user(request: HttpRequest) -> Response:
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(
            {'message': 'User successfully created, auth credentials will be sent on given email'},
            status=status.HTTP_201_CREATED)
    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
