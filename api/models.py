from django.db import models

class Genre(models.Model):

    title = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.title


class Movie(models.Model):

    title = models.CharField(max_length=500)
    year = models.FloatField()
    rating = models.FloatField()
    imdb_id = models.CharField(max_length=500)
    genre = models.ManyToManyField(Genre)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title
