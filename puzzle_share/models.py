from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

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
    name = models.CharField(max_length=30)
    pieces = models.PositiveSmallIntegerField(choices=PIECES, default= 500,)
    company = models.CharField(max_length=20)#, help_text = 'Enter name of puzzle manufacturer')
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1,)
    #status 1 = available; 0 means checked out
    owner_last_name = models.CharField(max_length=20)
    #when puzzle object created, checked out is set to blank; changes when puzzle is checked out
    user_last_name = models.CharField(max_length=20, default = "")
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)
    
    #may need to override save method if photo replaced; 
    #see wishlist/models
    
    class Meta:
        #to avoid duplicate puzzles being aded, and puzzles, name, pieces, and company together are a unique entity
        unique_together = [['name', 'pieces', 'company']]



    def delete_photo(self,photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo) #call method above
            #call through to Django super fx to do the actual delete
            super().delete(*args, **kwargs)

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'

        return f'{self.name} with {self.pieces} pieces from {self.company} owned by {self.owner_last_name}' 
