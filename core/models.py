from django.db import models
from django.contrib.auth.models import User
from .utilities import get_pub_path, get_priv_path


class Contest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    # TODO: renaming files & manage access (only for admins)
    public_reference_file = models.FileField(blank=True, null=True, upload_to=get_pub_path)
    private_reference_file = models.FileField(blank=True, null=True, upload_to=get_priv_path)


class Team(models.Model):
    name = models.CharField(max_length=100)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Attempt(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: renaming file
    file = models.FileField()
    public_score = models.FloatField(blank=True, null=True)
    private_score = models.FloatField(blank=True, null=True)
