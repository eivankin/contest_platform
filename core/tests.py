import datetime as dt
from .models import Contest, Team
from contest_platform.settings import BASE_DIR
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files import File


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
        response = self.client.get(reverse('core:all_contests'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_get_active_contests(self):
        response = self.client.get(reverse('core:contests', args=['active']))
        self.assertEqual(response.status_code, 200)
        contests_json = response.json()
        self.assertEqual(len(contests_json), 2)
        self.assertEqual(set(map(lambda x: x['name'], contests_json)), {'my', 'active'})

    def test_get_future_contests(self):
        response = self.client.get(reverse('core:contests', args=['future']))
        self.assertEqual(response.status_code, 200)
        contests_json = response.json()
        self.assertEqual(len(contests_json), 1)
        self.assertEqual(contests_json[0]['name'], 'future')

    def test_get_archive_contests(self):
        response = self.client.get(reverse('core:contests', args=['archive']))
        self.assertEqual(response.status_code, 200)
        contests_json = response.json()
        self.assertEqual(len(contests_json), 1)
        self.assertEqual(contests_json[0]['name'], 'archive')

    def test_get_my_contests(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:contests', args=['my']))
        self.assertEqual(response.status_code, 200)
        contests_json = response.json()
        self.assertEqual(len(contests_json), 1)
        self.assertEqual(contests_json[0]['name'], 'my')

    def test_get_nonexistent_contest_type(self):
        response = self.client.get(reverse('core:contests', args=['asdasd']))
        self.assertEqual(response.status_code, 404)


class AttemptViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.my_contest = Contest(
            name='my', description='test',
            starts_at=timezone.now() - dt.timedelta(days=1),
            ends_at=timezone.now() + dt.timedelta(days=1),
            public_reference_file=File(
                open(BASE_DIR / 'checker/tests_data/validation_points.zip', 'rb')),
            region_of_interest=File(open(BASE_DIR / 'checker/tests_data/roi.zip', 'rb')),
            column_to_compare='class'
        )
        cls.my_contest.save()
        cls.user = User(username='test')
        cls.user.save()

        cls.team = Team(name='test', contest=cls.my_contest)
        cls.team.save()
        cls.team.users.add(cls.user)
        cls.team.save()

    def test_submit_attempt_and_get_score(self):
        self.client.force_login(self.user)
        files = {'file': open(BASE_DIR / 'checker/tests_data/submit.zip', 'rb')}
        response = self.client.post(reverse('core:attempts', args=[self.my_contest.pk]), files)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'Attempt created successfully'})
        attempts = self.client.get(reverse('core:attempts', args=[self.my_contest.pk])).json()
        self.assertEqual(len(attempts), 1)
        self.assertEqual(attempts[0]['status'], 'Accepted')
        self.assertEqual(attempts[0]['public_score'], 1)

    def tearDown(self) -> None:
        self.user.delete()
        self.my_contest.delete()
