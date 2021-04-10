from django.urls import path
from core import views

urlpatterns = [
    path('contests/', views.contests),
    path('contests/<str:contests_type>', views.contests)
]