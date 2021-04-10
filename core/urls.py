from django.urls import path
from core import views

urlpatterns = [
    path('contests/', views.contests),
    path('contests/<str:contests_type>', views.contests),
    path('attempts/', views.attempts),
    path('attempts/<int:contest_id>', views.attempts)
]
