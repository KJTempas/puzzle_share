from django.urls import path
from . import views

urlpatterns = [
    path('', views.puzzle_list, name='puzzle_list'),
    path('checked_out', views.puzzles_checked_out, name='puzzles_checked_out')
]