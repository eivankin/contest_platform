from django.urls import path
from core import views

urlpatterns = [
    path('contests/', views.contests, name='all_contests'),
    path('contests/<int:contest_id>', views.contests, name='contest'),
    path('contests/<str:contests_type>', views.contests, name='contests'),
    path('attempts/', views.attempts, name='all_attempts'),
    path('attempts/<int:contest_id>', views.attempts, name='attempts'),
    path('teams/', views.teams, name='all_teams'),
    path('teams/<int:team_id>', views.teams, name='team'),
    path('teams/contest-<int:contest_id>', views.teams, name='teams'),
    path('get_permissions/<int:contest_id>', views.get_permissions, name='permissions'),
    path('users/', views.register_user, name='register_user')
]
