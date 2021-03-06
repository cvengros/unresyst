"""Demo models for the demo application"""

from django.db import models

from constants import *

class ShoePair(models.Model):
    """A model for a pair of shoes."""
    
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    """The shoe model name"""
    
    manufacturer = models.ForeignKey('Manufacturer', null=True)
    """The manufacturer who made the shoes."""
    
    for_winter = models.BooleanField(default=False)
    """Are the shoes suitable for winter?"""
    
    keywords = models.ManyToManyField('Keyword')
    """The keywords associated with the shoes."""

    image_path = models.CharField(max_length=MAX_LENGTH_IMAGE_PATH)
    """The path to the shoe image, relative to the MEDIA_ROOT"""
    
    category = models.ForeignKey('ShoeCategory', null=True)
    """The category where the shoe pair belongs"""
    
    def get_avatar_path(self):
        return self.image_path
    
    def __unicode__(self):
        """Return a printable representation of the instance"""
        return self.name    


class ShoeCategory(models.Model):    
    """A category of shoes, like casual, sport, ..."""
    
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    """The shoe category name"""

    def __unicode__(self):
        """Return a printable representation of the instance"""
        return self.name


class Keyword(models.Model):
    """A model for a keyword associated with shoe pair."""
    
    word = models.CharField(max_length=MAX_LENGTH_NAME, unique=True)
    """The key word."""    

    def __unicode__(self):
        """Return a printable representation of the instance"""
        return self.word

class User(models.Model):
    """A model for the users of the demo system."""

    name = models.CharField(max_length=MAX_LENGTH_NAME)
    """The user's name"""

    age = models.PositiveIntegerField(null=True, default=None)
    """The age of the user."""
    
    likes_shoes = models.ManyToManyField('ShoePair', related_name='likers')
    """User's favorite shoes."""
    
    viewed_shoes = models.ManyToManyField('ShoePair', related_name='viewers')
    """Shoes the user has viewed."""
    
    home_city = models.ForeignKey('City', null=True, default=None)        
    """The city where the user lives."""
    
    words_searched = models.ManyToManyField('Keyword', related_name='searchers')
    """The words searched by the user."""
    
    def __unicode__(self):
        """Return a printable representation of the instance"""
        return self.name

class ShoeRating(models.Model):
    """An explicit rating by user to a shoe pair"""
    
    user = models.ForeignKey('User')
    """The rater"""
    
    shoe_pair = models.ForeignKey('ShoePair')
    """The rated shoe pair"""
    
    stars = models.PositiveIntegerField()
    """Number of stars from 0 to 5 given to the shoepair"""

    class Meta:
        unique_together = ('user', 'shoe_pair')
        """There can be only one rating from a user to a shoe pair"""
    
    def __unicode__(self):
        """Return a printable representation of the instance"""
        return u"%s: %s (%d)" % (self.user, self.shoe_pair, self.stars)    
            

class Manufacturer(models.Model):
    """A model for a shoe manufacturer"""
    
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    """The name of the manufacturer"""
    
    home_city = models.ForeignKey('City', null=True)
    """The city where the manufacturer seats."""
    
    def __unicode__(self):
        """Return a printable representation of the instance"""
        return self.name    


class City(models.Model):
    """A model for a city."""    
        
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    """The name of the city."""
    
    in_south = models.BooleanField(default=False)
    """Is the city in south?"""
    
    def __unicode__(self):
        """Return a printable representation of the instance"""
        return self.name    
