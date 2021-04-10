from django.db import models
from django.contrib.auth.models import User
from .utilities import get_pub_path, get_priv_path, get_attempt_path


class Contest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    public_reference_file = models.FileField(blank=True, null=True, upload_to=get_pub_path)
    private_reference_file = models.FileField(blank=True, null=True, upload_to=get_priv_path)
    column_to_compare = models.CharField(max_length=50, null=True)


class Team(models.Model):
    name = models.CharField(max_length=100)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)


class Attempt(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=get_attempt_path)
    public_score = models.FloatField(blank=True, null=True)
    private_score = models.FloatField(blank=True, null=True)


def send_password_on_save(instance: User):
    if instance.password == '':
        password = User.objects.make_random_password()
        instance.set_password(password)
        instance.email_user(
            'Registration', f'Your auth credentials are:\nUsername: '
                            f'{instance.username}\nPassword: {password}')
    super(User, instance).save()


User.save = send_password_on_save
