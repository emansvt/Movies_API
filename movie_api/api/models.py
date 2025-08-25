from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxValueValidator
# Create your models here.

class Review(models.Model):
    movie_title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)
    