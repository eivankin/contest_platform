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
    return render(
        request, 'contests.html',
        {'title': 'Соревнования', 'active_contests': active_contests}
    )


def teams(request: HttpRequest) -> HttpResponse:
    pass
