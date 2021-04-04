from django.db import models


class Contest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    # TODO: renaming files & manage access (only for admins)
    public_reference_file = models.FileField(blank=True, null=True)
    private_reference_file = models.FileField(blank=True, null=True)


class Team(models.Model):
    name = models.CharField(max_length=100)
    leader_email = models.EmailField()
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE)
    password = models.CharField(max_length=100)


class Attempt(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: renaming file
    file = models.FileField()
    public_score = models.DecimalField(decimal_places=5, blank=True, null=True)
    private_score = models.DecimalField(decimal_places=5, blank=True, null=True)
