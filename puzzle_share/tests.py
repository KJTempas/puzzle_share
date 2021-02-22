import tempfile
import filecmp
import os

from django.test import TestCase
from django.urls import reverse
from django.test import override_settings

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from .models import Puzzle

from PIL import Image

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
    def setUp(self):
        self.MEDIA_ROOT = tempfile.mkdtemp()

    def tearDown(self):
        print('todo delete temp directory, temp image')

    def create_temp_image_file(self):
        handle, tmp_img_file = tempfile.mkstemp(suffix='.jpg')
        img = Image.new('RGB', (10, 10) )
        #save image to the file
        img.save(tmp_img_file, format='JPEG')
        return tmp_img_file
    
    
    def test_add_puzzle_no_photo(self):
        new_puzzle = {
            'name': 'Garden',
            'pieces': 500,
            'company': 'Ravensburger',
            'owner_last_name': 'Tempas'
        }

        response = self.client.post(reverse('add_puzzle'), data = new_puzzle, follow=True)
        #follow = true means follow redirect in method
        #did it redirect to puzzle list
        self.assertTemplateUsed('puzzle_share/puzzlelist.html')
        #does puzzlelist show new puzzle
        self.assertContains(response, 'Garden')
        self.assertContains(response, 500)
        #self.assertContains(response, 'Ravensburger') #TODO figure out why these 2 are not in the response
        #self.assertContains(response, 'Tempas')
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
        self.assertEqual('Tempas', puzzle.owner_last_name)

    def test_add_puzzle_with_image(self): #see wishlist tests - but they upload from details pg; I upload when adding puzzle
        img_file_path = self.create_temp_image_file()
        new_puzzle = {
                'name': 'Garden',
                'pieces': 500,
                'company': 'Ravensburger',
                'owner_last_name': 'Tempas',
                'photo': 'rb' #not sure about this part
                }
        with self.settings(MEDIA_ROOT=self.MEDIA_ROOT):
            with open(img_file_path, 'rb') as img_file:
                response = self.client.post(reverse('add_puzzle'), data = new_puzzle, follow=True)
                
                self.assertEqual(200, response.status_code)

#TODO - test can't add duplicate puzzles - not working
    # def test_duplicate_puzzle_does_not_add_to_dbase(self):
    #     #transaction atomic means dbase will be rolled back to previous if add not successful
    #     with transaction.atomic():
    #         new_puzzle = {
    #             'name': 'Garden',
    #             'pieces': 500,
    #             'company': 'Ravensburger',
    #             'owner_last_name': 'Tempas'
    #         }
    #         Puzzle.objects.create(**new_puzzle) #unpack dictionary above to create new puzzle object
    #         puzzle_count = Puzzle.objects.count()
    #         self.assertEqual(1, puzzle_count)   

    #     with transaction.atomic():
    #         #try to add puzzle again
    #         response = self.client.post(reverse('add_puzzle'), data = new_puzzle)#, follow=True)
    #         messages = response.context['messages']
    #         message_texts = [ message.message for message in messages ]
    #         self.assertIn('You already added that puzzle', message_texts)
    #     #still one puzzle in dbase
    #     puzzle_count = Puzzle.objects.count()    
    #     self.assertEqual(1, puzzle_count)   

     
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

class TestUserName(TestCase):

    def test_user_name_added_when_puzzle_checked_out(self):
        pass#use fixtures?

    def test_user_name_deleted_when_puzzle_returned(self):
        pass
        # p1 = Puzzle.objects.create(name='Perennials', pieces = 1000, company = 'GardenPuzzles', owner_last_name = "Tempas")
        # user_last_name = "Jilka"
        # response = self.client.get(reverse('puzzle_checked_out', args=(p1,)),follow=True)))


    
    