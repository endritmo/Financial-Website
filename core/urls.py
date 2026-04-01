from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('charts/', views.charts, name='charts'),
    path('calendar/', views.calendar, name='calendar'),
]
