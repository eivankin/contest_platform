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


class ActiveContestAttemptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attempt
        fields = ['team_id', 'status', 'created_at', 'public_score']


class ArchiveContestAttemptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attempt
        fields = ['team_id', 'status', 'created_at', 'public_score', 'private_score']


class NewAttemptSerializer(serializers.HyperlinkedModelSerializer):
    team_id = serializers.IntegerField()

    class Meta:
        model = Attempt
        fields = ['file', 'team_id']

    def create(self, validated_data):
        team = Team.objects.get(pk=validated_data.pop('team_id'))
        return Attempt(**validated_data, team=team)
