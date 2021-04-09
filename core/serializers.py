from .models import Contest, Team, Attempt
from rest_framework import serializers


class ContestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contest
        fields = ['name', 'description', 'starts_at', 'ends_at']


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'contest']


class AttemptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attempt
        fields = ['team', 'created_at', 'public_score']
