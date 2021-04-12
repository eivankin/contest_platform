import re
import os
from functools import lru_cache
from django.test import Client
from django.contrib import messages
from requests import get

API_KEY = os.getenv('GEOCODER_API_KEY')


def replace_geocode_tag(match: re.Match) -> str:
    return f'<br><img style="max-width: 100%" ' \
           f'src="https://static-maps.yandex.ru/1.x/{get_params(match.group(1))}"><br>'


@lru_cache(maxsize=2048)
def get_params(place: str):
    obj = get(
        'https://geocode-maps.yandex.ru/1.x/',
        params={'apikey': API_KEY, 'format': 'json', 'geocode': place}
    ).json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    bounds = obj['boundedBy']['Envelope']
    (x0, y0), (x1, y1) = map(lambda x: map(float, x.split()), bounds.values())
    return f'?l=sat,skl&ll={obj["Point"]["pos"].replace(" ", ",")}' \
           f'&spn={abs(x1 - x0)},{abs(y1 - y0)}'


def process_contest_data(contest_list: list) -> None:
    for contest in contest_list:
        contest['description'] = re.sub(
            r'@geocode\((\"[\w\s]+\")\)', replace_geocode_tag, contest['description'])


def prepare_client(user) -> Client:
    c = Client()
    if user.is_authenticated:
        c.force_login(user)
    return c


def repr_errors(errors: dict) -> str:
    return 'Ошибки: ' + ', '.join([f'{key} - {value[0].lower()[:-1]}'
                                  for key, value in errors.items()])


def repr_result(response, request, correct_status_code=201) -> None:
    if response.status_code == correct_status_code:
        messages.success(request, response.json()['message'])
    else:
        messages.error(request, repr_errors(response.json()))
