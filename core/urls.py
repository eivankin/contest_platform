from django.urls import path
from core import views

urlpatterns = [
    path('contests/', views.contests, name='all_contests'),
    path('contests/<str:contests_type>', views.contests, name='contests'),
    path('attempts/', views.attempts, name='all_attempts'),
    path('attempts/<int:contest_id>', views.attempts, name='attempts'),
    path('teams/', views.teams, name='all_teams'),
    path('teams/<int:contest_id>', views.teams, name='teams')
]
