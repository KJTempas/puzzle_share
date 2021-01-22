from django.shortcuts import render, redirect
from .models import Puzzle
from .forms import NewPuzzleForm

# Create your views here.

'''If this is a POST request, the user clicked the Add button
in the form. Check if the new puzzle is valid, if so, save a
new Puzzle to the dbase, and redirect to this same page.
This creates a GET request to this same route

If not a POST route, or Puzzle is not valid,display a page with
a list of puzzles and a form to add a new puzzle
'''

def puzzle_list(request):
    if request.method == 'POST':
        form = NewPuzzleForm(request.POST) 
        puzzle = form.save()#create a new Puzzle from the form
        if form.is_valid(): #check against DB constraints
            puzzle.save() #save Puzzle to the dbase
            return redirect('puzzle_list') #redirects to GET view w puzzle list (same view)

#If not a POST, or formis not valid, render the page with empty form
    puzzles = Puzzle.objects.filter(status = True).order_by('name')
    new_puzzle_form = NewPuzzleForm()
    return render(request, 'puzzle_share/puzzlelist.html', { 'puzzles': puzzles, 'new_puzzle_form': new_puzzle_form })


def puzzles_checked_out(request):
    status = Puzzle.objects.filter(status = 2)
    return render(request, 'puzzle_share/checked_out.html', { 'status': status})
    