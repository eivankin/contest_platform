from django.urls import path
from front import views

urlpatterns = [
    path('contests/', views.contests, name='contests'),
    path('contests/<int:contest_id>/', views.contest, name='contest'),
    path('teams/', views.teams, name='teams')
]
