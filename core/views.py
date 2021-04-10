from django.http import HttpRequest
from django.utils import timezone
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Team, Contest, Attempt
from .serializers import TeamSerializer, ContestSerializer, \
    ActiveContestAttemptSerializer, ArchiveContestAttemptSerializer, NewAttemptSerializer


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
def contests(request: HttpRequest, contests_type: str = 'all') -> Response:
    """Main contest view, returns json dictionary with requested contests or 404."""
    contests_types = {'all': lambda: Contest.objects.all(),
                      'active': active_contests,
                      'archive': archive_contests,
                      'future': future_contests,
                      'my': active_contests}
    if contests_type not in contests_types:
        return Response(status=status.HTTP_404_NOT_FOUND)
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
            return Response(status=status.HTTP_404_NOT_FOUND)

        if contest.starts_at > timezone.now() or contest.ends_at < timezone.now():
            return Response({'message': 'you can\'t create attempt in inactive contest'},
                            status=status.HTTP_403_FORBIDDEN)

        data = {'team_id': request.user.team_set.get(contest=contest).pk,
                'file': request.FILES.get('file')}
        serialized = NewAttemptSerializer(data=data)
        if serialized.is_valid():
            instance = serialized.save()
            instance.save()
            return Response({'message': 'saved successfully'}, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def teams(request: HttpRequest, contest_id: int = None) -> Response:
    """
    Returns list of user teams if contest_id is None,
    else returns all teams registered on contest
    """
    if contest_id is None:
        teams_query = request.user.team_set.all()
    else:
        teams_query = Team.objects.filter(contest_id=contest_id)
    serialized = TeamSerializer(teams_query, many=True)
    return Response(serialized.data)


@api_view(['GET'])
def leaderboard(request: HttpRequest, contest_id: int) -> Response:
    """
    Returns list of teams with their best score.
    If contest is finished, returns public and private leaderboard,
    otherwise only public leaderboard will be returned.
    """
    pass
