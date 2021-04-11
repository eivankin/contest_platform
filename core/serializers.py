from .models import Contest, Team, Attempt
from rest_framework import serializers


class ContestSerializer(serializers.HyperlinkedModelSerializer):
    starts_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    ends_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = Contest
        fields = ['id', 'name', 'description', 'starts_at', 'ends_at']


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    score = serializers.FloatField(required=False)
    users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'contest_id', 'score', 'users']


class ActiveContestAttemptSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Attempt
        fields = ['team_id', 'status', 'created_at', 'public_score']


class ArchiveContestAttemptSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")

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
