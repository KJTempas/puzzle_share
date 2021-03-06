from django.urls import path
from . import views

urlpatterns = [
    path('', views.puzzle_list, name='puzzle_list'),
    path('checked_out', views.puzzles_checked_out, name='puzzles_checked_out'),
    path('puzzle/<int:puzzle_pk>/checked_out/', views.puzzle_checked_out, name='puzzle_checked_out'),
    path('puzzle/<int:puzzle_pk>/returned/', views.puzzle_returned, name='puzzle_returned'),
    path('available', views.puzzles_available, name='puzzles_available'),
    path('add_puzzle', views.add_puzzle, name='add_puzzle'),
    path('puzzle/<int:puzzle_pk>', views.puzzle_details, name='puzzle_details'),
    path('puzzle/<int:puzzle_pk>/delete', views.delete_puzzle, name='delete_puzzle'),
    #path('puzzle/<int:puzzle_pk>/edit', views.edit_puzzle_details, name='edit_puzzle_details')
]