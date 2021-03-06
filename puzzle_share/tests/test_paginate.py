from django.test import TestCase
from puzzle_share import helpers
from puzzle_share.models import Puzzle


class TestListWithPageData(TestCase):

    #setup will provide sample data to the dbase; data created every time test
    #are run and destroyed at end of test
    def setUp(self):
        for i in range(5): #create and save 5 puzzles to dbase
            puzzle = Puzzle(name = f'name{i+1}', pieces = 500, company = f'comp{i+1}', status = 1, owner_last_name = f'oln{i+1}')
            puzzle.save()

    #check that puzzle names on first page are correct
    def test_first_page_lists_correct_puzzle_names(self):
        puzzles = Puzzle.objects.all().order_by('name')
                                    # request, list of objects, how many entries perpage
        paged_list = helpers.pg_records(1, puzzles, 2)
        self.assertEqual(puzzles[0].name, paged_list[0].name)
        self.assertEqual(puzzles[1].name, paged_list[1].name)

    #check that correct number of puzzles are displayed on page 1
    def test_correct_number_of_puzzles_displayed_on_page_one(self):
        puzzles = Puzzle.objects.all().order_by('name')
        paged_list = helpers.pg_records(1, puzzles, 4) #display 4 puzzles per page
        self.assertEqual(len(paged_list), 4)

        #check that correct number of puzzles are displayed on page 2
        #4 puzzles per page means 4 go on pg 1 while 1 goes on page 2
    def test_correct_number_of_puzzles_displayed_on_page_two(self):
        puzzles = Puzzle.objects.all().order_by('name')
        paged_list = helpers.pg_records(2, puzzles, 4) #display 4 puzzles per page
        self.assertEqual(len(paged_list), 1)