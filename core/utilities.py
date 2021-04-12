import os


def get_attempt_path(instance, filename: str):
    return f'files/attempts/{instance.team.pk}/' \
           f'{int(instance.created_at.timestamp())}{os.path.splitext(filename)[1]}'
