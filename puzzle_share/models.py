from django.db import models
from django.contrib.auth.models import User

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
    #user = models.ForeignKey('auth.User', null=False, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    pieces = models.PositiveSmallIntegerField(choices=PIECES, default= 500,)
    company = models.CharField(max_length=20)#, help_text = 'Enter name of puzzle manufacturer')
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1,)
    #status 1 = available; 0 means checked out
    owner_last_name = models.CharField(max_length=20)
    #when puzzle object created, checked out is set to blank; changes when puzzle is checked out
    user_last_name = models.CharField(max_length=20, default = "")

    class Meta:
        #to avoid duplicate puzzles being aded, and puzzles, name, pieces, and company together are a unique entity
        unique_together = [['name', 'pieces', 'company']]
    def __str__(self):
        return f'{self.name} with {self.pieces} pieces from {self.company}' 
