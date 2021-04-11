from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.test import Client
from django.contrib import messages
from .utilities import process_contest_data


def contests(request: HttpRequest) -> HttpResponse:
    c = Client()
    c.force_login(request.user)
    my_contests = None
    if request.user.is_authenticated:
        my_contests = c.get(
            reverse('core:contests', args=['active'])).json()
        process_contest_data(my_contests)

    active_contests = c.get(
        reverse('core:contests', args=['active'])).json()
    process_contest_data(active_contests)
    if my_contests:
        my_ids = set(map(lambda x: x['id'], my_contests))
        active_contests = [c for c in active_contests if c['id'] not in my_ids]

    future_contests = c.get(
        reverse('core:contests', args=['future'])).json()
    process_contest_data(future_contests)

    archive_contests = c.get(
        reverse('core:contests', args=['archive'])).json()
    process_contest_data(archive_contests)

    return render(
        request, 'contests.html',
        {'title': 'Соревнования', 'my_contests': my_contests,
         'active_contests': active_contests, 'future_contests': future_contests,
         'archive_contests': archive_contests}
    )


def contest(request: HttpRequest, contest_id: int) -> HttpResponse:
    c = Client()
    c.force_login(request.user)
    contest_data = c.get(reverse('core:contest', args=[contest_id])).json()
    if 'message' in contest_data:
        messages.error(request, 'Error: ' + contest_data['message'])
        return redirect(reverse('front:contests'))
    process_contest_data([contest_data])
    permissions = c.get(reverse('core:permissions', args=[contest_id])).json()
    leaderboard = c.get(
        reverse('core:teams', args=[contest_id]), params={'order_by': 'public_score'}
    ).json()
    return render(request, 'contest.html', {
        'contest': contest_data, 'title': contest_data['name'],
        'teams': leaderboard, 'permissions': permissions})


def teams(request: HttpRequest) -> HttpResponse:
    pass