from django.http import JsonResponse, Http404, HttpRequest
from django.utils import timezone
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_exempt
from .models import Team, Contest, Attempt
from .serializers import TeamSerializer, ContestSerializer, AttemptSerializer


def active_contests() -> JsonResponse:
    """Returns QuerySet of active contests"""
    now = timezone.now()
    return Contest.objects.filter(ends_at__gt=now, starts_at__lte=now).order_by('-ends_at')


def archive_contests() -> QuerySet:
    """Returns QuerySet of archive contests"""
    return Contest.objects.filter(ends_at__lte=timezone.now()).order_by('-ends_at')


def future_contests():
    """Returns QuerySet of future contest"""
    return Contest.objects.filter(starts_at__gt=timezone.now()).order_by('-starts_at')


@csrf_exempt
def contests(request: HttpRequest, contests_type: str = 'all') -> JsonResponse:
    """Main contest view, returns json dictionary with requested contests or raises Http404"""
    contests_types = {'all': lambda: Contest.objects.all(),
                      'active': active_contests,
                      'archive': archive_contests,
                      'future': future_contests,
                      'my': active_contests}
    if contests_type not in contests_types:
        raise Http404
    contests_query = contests_types[contests_type]()
    if contests_type == 'my' and request.user.is_authenticated:
        contests_query = contests_query.filter(team__in=request.user.team_set.all())
    serializer = ContestSerializer(contests_query, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def attempts(request: HttpRequest, contest_id: int = None) -> JsonResponse:
    attempts_query = Attempt.objects.filter(team__in=request.user.team_set.all())
    if contest_id is not None:
        attempts_query = attempts_query.filter(team__contest_id=contest_id)
    serializer = AttemptSerializer(attempts_query, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def teams(request: HttpRequest) -> JsonResponse:
    pass
