import datetime as dt
from .models import Contest, Team
from django.test import TestCase
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User


class ContestViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        my_contest = Contest(name='my', description='test',
                             starts_at=timezone.now() - dt.timedelta(days=1),
                             ends_at=timezone.now() + dt.timedelta(days=1))
        my_contest.save()
        Contest(name='active', description='test',
                starts_at=timezone.now() - dt.timedelta(days=1),
                ends_at=timezone.now() + dt.timedelta(days=1)).save()
        Contest(name='archive', description='test',
                starts_at=timezone.now() - dt.timedelta(days=2),
                ends_at=timezone.now() - dt.timedelta(days=1)).save()
        Contest(name='future', description='test',
                starts_at=timezone.now() + dt.timedelta(days=1),
                ends_at=timezone.now() + dt.timedelta(days=2)).save()

        cls.user = User(username='test')
        cls.user.save()

        cls.team = Team(name='test', contest=my_contest)
        cls.team.save()
        cls.team.users.add(cls.user)
        cls.team.save()

    def test_get_all_contests(self):
        response: JsonResponse = self.client.get('/api/contests/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_get_active_contests(self):
        response = self.client.get('/api/contests/active')
        self.assertEqual(response.status_code, 200)
        contests_json = response.json()
        self.assertEqual(len(contests_json), 2)
        self.assertEqual(set(map(lambda x: x['name'], contests_json)), {'my', 'active'})

    def test_get_future_contests(self):
        response = self.client.get('/api/contests/future')
        self.assertEqual(response.status_code, 200)
        contests_json = response.json()
        self.assertEqual(len(contests_json), 1)
        self.assertEqual(contests_json[0]['name'], 'future')

    def test_get_archive_contests(self):
        response = self.client.get('/api/contests/archive')
        self.assertEqual(response.status_code, 200)
        contests_json = response.json()
        self.assertEqual(len(contests_json), 1)
        self.assertEqual(contests_json[0]['name'], 'archive')

    def test_get_my_contests(self):
        self.client.force_login(self.user)
        response = self.client.get('/api/contests/my')
        self.assertEqual(response.status_code, 200)
        contests_json = response.json()
        self.assertEqual(len(contests_json), 1)
        self.assertEqual(contests_json[0]['name'], 'my')
