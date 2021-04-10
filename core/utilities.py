import os


def get_attempt_path(instance, filename: str):
    return f'attempts/{instance.team.pk}/{instance.created_at}{os.path.splitext(filename)[1]}'
