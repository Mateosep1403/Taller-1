from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, default="sin descripción")
    image = models.ImageField(upload_to='movies/images/')
    url = models.URLField(blank=True)