from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.test import Client
from .utilities import process_contest_data


def contests(request: HttpRequest) -> HttpResponse:
    c = Client()
    active_contests = c.get(
        reverse('core:contests', args=['active'])).json()
    process_contest_data(active_contests)

    future_contests = c.get(
        reverse('core:contests', args=['future'])).json()
    process_contest_data(future_contests)

    archive_contests = c.get(
        reverse('core:contests', args=['archive'])).json()
    process_contest_data(archive_contests)

    return render(
        request, 'contests.html',
        {'title': 'Соревнования', 'active_contests': active_contests,
         'future_contests': future_contests, 'archive_contests': archive_contests}
    )


def teams(request: HttpRequest) -> HttpResponse:
    pass
