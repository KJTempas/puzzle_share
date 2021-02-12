from django.shortcuts import render, redirect, get_object_or_404
from .models import Puzzle
from django.contrib import messages
from .forms import NewPuzzleForm, SearchForm, NameForm
from django.db import IntegrityError

# Create your views here.

'''If this is a POST request, the user clicked the Add button
in the form. Check if the new puzzle is valid, if so, save a
new Puzzle to the dbase, and redirect to this same page.
This creates a GET request to this same route

If not a POST route, or Puzzle is not valid,display a page with
a list of puzzles and a form to add a new puzzle
'''

def add_puzzle(request):
    if request.method == 'POST':
        form = NewPuzzleForm(request.POST, request.FILES) 
        puzzle = form.save()#create a new Puzzle from the form
        if form.is_valid(): #check against DB constraints(which includes uniqueTogether)
            try: #check if this puzzle is already in dbase; if so do not readd
                puzzle = Puzzle.objects.get(name = name, pieces = pieces, company = company)#), owner_last_name = owner_last_name)
            except:
                puzzle.save() #save Puzzle to the dbase

            return redirect('puzzle_list') #redirects to GET view w puzzle list (same view)
     

#If not a POST, (so a GET) or form is not valid, render the page with empty form
    puzzles = Puzzle.objects.order_by('name')
    new_puzzle_form = NewPuzzleForm()
    return render(request, 'puzzle_share/add.html', { 'puzzles': puzzles, 'new_puzzle_form': new_puzzle_form })

def puzzle_list(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        puzzles = Puzzle.objects.filter(name__icontains=search_term).order_by('name')
    else:
        search_form = SearchForm()
        puzzles = Puzzle.objects.order_by('name')

    return render(request, 'puzzle_share/puzzlelist.html', {'puzzles': puzzles, 'search_form': search_form})

def puzzles_available(request):
    status = Puzzle.objects.filter(status=1).order_by('name')
    return render(request, 'puzzle_share/available.html', { 'status': status})

#TODO change name of this method to all_puzzles.....
def puzzles_checked_out(request): #list of currently checked outpuzzles
    status = Puzzle.objects.filter(status = 2).order_by('name')
    return render(request, 'puzzle_share/checked_out.html', { 'status': status})
    
#the following two methods change status of puzzles from avail to checked out or back
def puzzle_checked_out(request, puzzle_pk): #change from available to checked out
    #if a POST request, need to process the form data
    if request.method == 'POST':
        #create form instance and populate w/ data from request
        form = NameForm(request.POST)
        #check whether data is valid (not empty)
        #checked_out = form.save()
        if form.is_valid(): #then process data
            user_last_name = form.cleaned_data['user_last_name']
            #get puzzle with pk and update it's fields
            puzzle = get_object_or_404(Puzzle, pk=puzzle_pk) 
            puzzle.status = 2 #2 means checked out; 1 is available
            puzzle.user_last_name = user_last_name 
            puzzle.save()

    else: #if a GET (or other method), create a blank form
        form = NameForm()

    return redirect('puzzle_list')


def puzzle_returned(request, puzzle_pk):
    if request.method =='POST':
        puzzle = Puzzle.objects.get(pk=puzzle_pk)
        puzzle.status = 1
        puzzle.user_last_name = ""
        puzzle.save()
    
    return redirect('puzzle_list')


def puzzle_details(request, puzzle_pk):
    puzzle = get_object_or_404(Puzzle, pk=puzzle_pk)
    return render(request, 'puzzle_share/puzzle_details.html', {'puzzle': puzzle} )

def delete_puzzle(request, puzzle_pk):
    puzzle = get_object_or_404(Puzzle, pk=puzzle_pk)
    puzzle.delete()
    return redirect('puzzle_list')

#TODO add pagination feature