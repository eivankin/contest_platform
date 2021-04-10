from django.urls import path
from front import views

urlpatterns = [
    path('contests/', views.contests, name='contests'),
    path('teams/', views.teams, name='teams')
]
