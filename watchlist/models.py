from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class StreamingPlatform(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=300)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class Movies(models.Model):
    Mname = models.CharField(max_length=100)
    Mdesc = models.CharField(max_length=300)
    isPublished = models.BooleanField(default=True)
    Mdate = models.DateField(auto_now_add=True)
    Splatform = models.ForeignKey(
        StreamingPlatform, on_delete=models.CASCADE, related_name='watchlist')

    def __str__(self):
        return self.Mname


class Reviews(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=100)
    Rdesc = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey(
        Movies, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.title
