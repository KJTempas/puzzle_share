from django.db import models

# Create your models here.

class Puzzle(models.Model):
    PIECES = (
        (50,  ('50 pieces or less')),
        (100, ('100 pieces')),
        (250, ('250 pieces')),
        (500, ('500 pieces')),
        (750, ('750 pieces')),
        (1000, ('1000 pieces'))
    )
    STATUS=(
        (1, ('Available to borrow')),
        (2, ('Borrowed by someone')),
    )
    name = models.CharField(max_length=20)
    pieces = models.PositiveSmallIntegerField(choices=PIECES, default= 500,)
    company = models.CharField(max_length=20)#, help_text = 'Enter name of puzzle manufacturer')
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1,)
    #status 1 = available; 0 means checked out
    def __str__(self):
        return f'{self.name} with {self.pieces} pieces from {self.company}' #is available? {self.status}'
