from django.urls import path
from front import views

urlpatterns = [
    path('contests/', views.contests, name='contests'),
    path('contests/<int:contest_id>/', views.contest, name='contest'),
    path('contests/<int:contest_id>/attempts', views.attempts, name='attempts'),
    path('teams/', views.teams, name='teams'),
    path('contests/<int:contest_id>/teams', views.teams, name='contest_teams'),
    path('register', views.register, name='register_user'),
    path('contests/<int:contest_id>/register', views.register, name='register_team'),
    path('teams/<int:team_id>/join', views.join_team, name='join_team')
]
