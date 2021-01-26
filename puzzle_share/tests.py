import tempfile
import filecmp
import os

from django.test import TestCase
from django.urls import reverse
from django.test import override_settings

from django.contrib.auth.models import User
from .models import Puzzle

# Create your tests here.

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
    #fixtures are loaded into the dbase for all tests in this class
    fixtures = ['test_puzzles', 'test_users']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_view_puzzlelist(self):
        response = self.client.get(reverse('puzzle_list'))
        #make sure correct template used
        self.assertTemplateUsed(response, 'puzzle_share/puzzlelist.html')
#TODO fix this part - problem wit user
        # data_rendered = list(response.context['puzzles'])
        # #data in dbase; get all puzzles in fixtures
        # data_expected = list(Puzzle.objects).filter(user=self.user))

        # self.assertCountEqual(data_rendered, data_expected)

    # def test_puzzles_checked_out(self):
    #     response = self.client.get(reverse('puzzles_checked_out'))
    #     #correct template used?
    #     self.assertTemplateUsed(response, 'puzzle_share/checked_out.html')

    #     #what data sent to template
    #     data_rendered = list(response.context['status' == 2])
    #     #data in dbase
    #     data_expected = list(Puzzle.objects.filter(user=self.user).filter(status=2))
    #     #same number?
    #     self.assertCountEqual(data_rendered, data_expected)