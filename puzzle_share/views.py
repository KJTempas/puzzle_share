from django.shortcuts import render, redirect, get_object_or_404
from .models import Puzzle
from .forms import NewPuzzleForm, SearchForm

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
        form = NewPuzzleForm(request.POST) 
        puzzle = form.save()#create a new Puzzle from the form
        if form.is_valid(): #check against DB constraints
            puzzle.save() #save Puzzle to the dbase
            return redirect('puzzle_list') #redirects to GET view w puzzle list (same view)

#If not a POST, or form is not valid, render the page with empty form
    puzzles = Puzzle.objects.order_by('name')
    new_puzzle_form = NewPuzzleForm()
    return render(request, 'puzzle_share/puzzlelist.html', { 'puzzles': puzzles, 'new_puzzle_form': new_puzzle_form })

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
    status = Puzzle.objects.filter(status=True).order_by('name')
    return render(request, 'puzzle_share/available.html', { 'status': status})

def puzzles_checked_out(request): #list of currently checked outpuzzles
    status = Puzzle.objects.filter(status = 2).order_by('name')
    return render(request, 'puzzle_share/checked_out.html', { 'status': status})
    

def puzzle_was_checked_out(request, puzzle_pk): #change from available to checked out
    if request.method == 'POST':
        puzzle = get_object_or_404(Puzzle, pk=puzzle_pk) 
        puzzle.status = 2 #2 means checked out; 1 is available
        puzzle.save()
    
    return redirect('puzzle_list')

def puzzle_returned(request, puzzle_pk):
    if request.method =='POST':
        puzzle = Puzzle.objects.get(pk=puzzle_pk)
        puzzle.status = 1
        puzzle.save()
    
    return redirect('puzzle_list')
