from rest_framework import viewsets
from rest_framework import permissions
from .models import Team, Contest, Attempt
from .serializers import TeamSerializer, ContestSerializer, AttemptSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all().order_by('-starts_at')
    serializer_class = ContestSerializer
    permission_classes = [permissions.IsAuthenticated]


class AttemptViewSet(viewsets.ModelViewSet):
    queryset = Attempt.objects.all().order_by('-created_at')
    serializer_class = AttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
