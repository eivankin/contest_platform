from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from .utilities import get_attempt_path
from checker.main import calc_score


class Contest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    region_of_interest = models.FileField(upload_to='files/contests/%Y/%m/%d/',
                                          null=True, blank=True)
    public_reference_file = models.FileField(blank=True, null=True,
                                             upload_to='files/contests/%Y/%m/%d/')
    private_reference_file = models.FileField(blank=True, null=True,
                                              upload_to='files/contests/%Y/%m/%d/')
    column_to_compare = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Attempt(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='On checking', editable=False)
    file = models.FileField(upload_to=get_attempt_path)
    public_score = models.FloatField(null=True, editable=False)
    private_score = models.FloatField(null=True, editable=False)

    def __str__(self):
        return f'{self.team} {self.created_at}'


def send_password_on_save(instance: User, *args, **kwargs):
    if instance.password == '':
        password = User.objects.make_random_password()
        instance.set_password(password)
        instance.email_user(
            'Registration', f'Your auth credentials are:\nUsername: '
                            f'{instance.username}\nPassword: {password}')
    super(User, instance).save(*args, **kwargs)


User.save = send_password_on_save


@receiver(post_save, sender=Attempt)
def calculate_score_after_save(sender, instance: Attempt, **kwargs):
    if instance.status == 'On checking':
        contest = instance.team.contest
        if contest.public_reference_file.name != '':
            try:
                instance.public_score = calc_score(
                    contest.column_to_compare, instance.file.path,
                    contest.public_reference_file.path, contest.region_of_interest.path)
                instance.status = 'Accepted'
            except Exception as e:
                instance.status = 'Error: ' + str(e)
            instance.save()
        if contest.private_reference_file.name != '' and not instance.status.startswith('Error'):
            try:
                instance.private_score = calc_score(
                    contest.column_to_compare, instance.file.path,
                    contest.public_reference_file.path, contest.region_of_interest.path)
                instance.status = 'Accepted'
            except Exception as e:
                instance.status = 'Error: ' + str(e)
            instance.save()

        if instance.status == 'On checking':
            instance.status = 'Accepted'
            instance.save()


@receiver(post_delete, sender=Attempt)
def delete_attempt_file(sender, instance: Attempt, **kwargs):
    instance.file.delete(False)


@receiver(post_delete, sender=Contest)
def delete_contest_files(sender, instance: Contest, **kwargs):
    instance.public_reference_file.delete(False)
    instance.private_reference_file.delete(False)
    instance.region_of_interest.delete(False)
