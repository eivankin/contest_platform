import os


def get_pub_path(instance, filename: str) -> str:
    return get_path(instance.pk, os.path.splitext(filename)[1], 'public')


def get_priv_path(instance, filename: str) -> str:
    return get_path(instance.pk, os.path.splitext(filename)[1], 'private')


def get_path(contest_id: int, file_ext: str, file_type: str) -> str:
    return f'contests/{contest_id}/{file_type}{file_ext}'


def get_attempt_path(instance, filename: str):
    return f'attempts/{instance.team.pk}/{instance.pk}{os.path.splitext(filename)[1]}'
