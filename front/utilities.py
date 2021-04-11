import re
import os
from functools import lru_cache
from requests import get

API_KEY = os.getenv('GEOCODER_API_KEY')


@lru_cache(maxsize=2048)
def replace_geocode_tag(match: re.Match) -> str:
    return f'<br><img src="https://static-maps.yandex.ru/1.x/{get_params(match.group(1))}">'


def get_params(place: str):
    obj = get(
        'https://geocode-maps.yandex.ru/1.x/',
        params={'apikey': API_KEY, 'format': 'json', 'geocode': place}
    ).json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    bounds = obj['boundedBy']['Envelope']
    (x0, y0), (x1, y1) = map(lambda x: map(float, x.split()), bounds.values())
    return f'?l=sat&ll={obj["Point"]["pos"].replace(" ", ",")}&spn={abs(x1 - x0)},{abs(y1 - y0)}'


def process_contest_data(contest_list: list) -> None:
    for contest in contest_list:
        contest['description'] = re.sub(
            r'@geocode\((.*)\)', replace_geocode_tag, contest['description'])