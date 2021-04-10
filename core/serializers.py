from .models import Contest, Team, Attempt
from rest_framework import serializers


class ContestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contest
        fields = ['id', 'name', 'description', 'starts_at', 'ends_at']


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'contest_id']


class AttemptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attempt
        fields = ['team_id', 'status', 'created_at', 'public_score']
