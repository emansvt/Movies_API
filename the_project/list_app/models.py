from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
#Sobre el User model: https://docs.djangoproject.com/en/5.1/ref/contrib/auth/
from django.contrib.auth.models import User

# Create your models here.
class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about= models.CharField(max_length=250)
    website = models.URLField(max_length=500)

    #en el admin panel regresar un string con el nombre
    def __str__(self) -> str:
        return self.name

class WatchList(models.Model):
    title = models.CharField(max_length=200)
    storyline = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    avg_rating = models.FloatField(default=0)
    number_ratings = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title
    
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    #conectamos con watchlist
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")

    #título en el admin panel
    def __str__(self) -> str:
        return str(self.rating) + " - " + self.watchlist.title + " - " + str(self.review_user)