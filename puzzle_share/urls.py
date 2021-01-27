from django.urls import path
from . import views

urlpatterns = [
    path('', views.puzzle_list, name='puzzle_list'),
    path('checked_out', views.puzzles_checked_out, name='puzzles_checked_out'),
    path('puzzle/<int:puzzle_pk>/checked_out/', views.puzzle_was_checked_out, name='puzzle_checked_out'),
    path('puzzle/<int:puzzle_pk>/returned/', views.puzzle_returned, name='puzzle_returned'),
    path('available', views.puzzles_available, name='puzzles_available'),
    path('add_puzzle', views.add_puzzle, name='add_puzzle')
]