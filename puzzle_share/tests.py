import tempfile
import filecmp
import os

from django.test import TestCase
from django.urls import reverse
from django.test import override_settings

from django.contrib.auth.models import User
from .models import Puzzle



class TestViewHomePageIsEmptyList(TestCase):

    fixtures = ['test_users']

    def setUp(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)

    def test_load_puzzlelist_page_shows_empty_list(self):
        response = self.client.get(reverse('puzzle_list'))
        self.assertTemplateUsed(response, 'puzzle_share/puzzlelist.html')
        self.assertEquals(0, len(response.context['puzzles']))

    def test_load_checked_out_page_shows_empty_list(self):
        response = self.client.get(reverse('puzzles_checked_out'))
        self.assertTemplateUsed(response, 'puzzle_share/checked_out.html')
        self.assertEquals(0, len(response.context['status']))

    def test_load_available_page_shows_empty_list(self):
        response = self.client.get(reverse('puzzles_available'))
        self.assertTemplateUsed(response, 'puzzle_share/available.html')
        self.assertEquals(0, len(response.context['status']))


class TestPuzzleList(TestCase):

    def test_view_puzzlelist_shows_all_in_expected_order(self):
        #all puzzles, both status 1(available) and 2(checked_out appear on main puzzle_list page)
        p1 = Puzzle.objects.create(name='Grasses', pieces = 500, company = 'GardenPuzzles', status = 1)
        p2 = Puzzle.objects.create(name='Grasses-Natives', pieces = 750, company = 'GardenPuzzles', status = 2)
        p3 = Puzzle.objects.create(name='Perennials', pieces = 1000, company = 'GardenPuzzles', status = 1)
        p4 = Puzzle.objects.create(name = 'Pasque Flower ', pieces = 250, company = 'GardenPuzzles', status = 2)

        expected_puzzle_order = [p1,p2,p4,p3]
        response = self.client.get(reverse('puzzle_list'))
        puzzles_in_template = list(response.context['puzzles'])
        self.assertEqual(expected_puzzle_order, puzzles_in_template)

    def test_only_puzzles_checked_out_appear_on_checked_out_page(self): 
        fixtures = ['test_puzzles']
    #     p1 = Puzzle.objects.create(name='Grasses', pieces = 500, company = 'GardenPuzzles', status = 1)
    #     p2 = Puzzle.objects.create(name='Grasses-Natives', pieces = 750, company = 'GardenPuzzles', status = 2)
    #     p3 = Puzzle.objects.create(name='Perennials', pieces = 1000, company = 'GardenPuzzles', status = 1)
    #     p4 = Puzzle.objects.create(name = 'Pasque Flower ', pieces = 250, company = 'GardenPuzzles', status = 2)

        

class TestAddPuzzle(TestCase):
    #add puzzle; add to dbase, puzzle ID created
    def test_add_puzzle(self):
        new_puzzle = {
            'name': 'Garden',
            'pieces': 500,
            'company': 'Ravensburger'
        }

        response = self.client.post(reverse('add_puzzle'), data = new_puzzle, follow=True)
        #follow = true means follow redirect in method
        #did it redirect to puzzle list
        self.assertTemplateUsed('puzzlew_share/puzzlelist.html')
        #does puzzlelist show new puzzle
        self.assertContains(response, 'Garden')
        self.assertContains(response, 500)
        self.assertContains(response, 'Ravensburger')
        self.assertContains(response, 1) #1 = status available and is default 
    
        #one puzzle in dbase
        puzzle_count = Puzzle.objects.count()
        self.assertEqual(1, puzzle_count)
        #retrieve that puzzle from dbase
        puzzle = Puzzle.objects.first()
        #check its properties
        self.assertEqual('Garden', puzzle.name)
        self.assertEqual(500, puzzle.pieces)
        self.assertEqual('Ravensburger', puzzle.company)


#TODO - test can't add duplicate puzzles(see videoApp)


class TestStatusChange(TestCase):
    fixtures = ['test_puzzles']

    def test_puzzle_changed_from_available_to_checked_out(self):
        # #change status of puzzle w PK of 3 to status2(checked_out)
        response = self.client.post(reverse('puzzle_checked_out', args=(3,)),follow=True)
        #assert redirects to puzzlelist
        self.assertTemplateUsed(response, 'puzzle_share/puzzlelist.html')
        #check dbase for correct data
        puzzle = Puzzle.objects.get(pk=3)
        self.assertEquals(2, puzzle.status) #1 is available, 2 is checked out


    def test_puzzle_changed_from_checked_out_to_available(self):
        # #change status of puzzle w PK of 2 from status 2(checked_out) to status1(available)
        response = self.client.post(reverse('puzzle_returned', args=(2,)),follow=True)
        #assert redirects to puzzlelist
        self.assertTemplateUsed(response, 'puzzle_share/puzzlelist.html')
        #check dbase for correct data
        puzzle = Puzzle.objects.get(pk=2)
        self.assertEquals(1, puzzle.status) #1 is available, 2 is checked out


class TestSearch(TestCase):

    def test_puzzle_search_matches_case_insensitive_and_partial(self): 
        #put 4 puzzles in cbase
        p1 = Puzzle.objects.create(name='Grasses', pieces = 500, company = 'GardenPuzzles')
        p2 = Puzzle.objects.create(name='Natives', pieces = 750, company = 'GardenPuzzles')
        p3 = Puzzle.objects.create(name='Perennials', pieces = 1000, company = 'GardenPuzzles')
        p4 = Puzzle.objects.create(name = 'Pasque Flower ', pieces = 250, company = 'GardenPuzzles')

        expected_video_order = [p4,p3] #searching for p should yield these 2 puzzles
        response = self.client.get(reverse('puzzle_list') + '?search_term=p')
        puzzles_in_template = list(response.context['puzzles'])
        self.assertEqual(expected_video_order, puzzles_in_template)


    def test_no_puzzles_match_message(self):
        response = self.client.get(reverse('puzzle_list'))
        puzzles_in_template = response.context['puzzles']
        self.assertContains(response, 'No puzzles')
        self.assertEquals(0, len(puzzles_in_template))