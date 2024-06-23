from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Places(models.Model):
    class Meta:
        verbose_name_plural = 'Places'

    name = models.CharField(max_length=30)
    story_field = models.TextField(blank=True)
    upload_picture = models.ImageField(upload_to='media/')
    location_map = models.CharField(max_length=40)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    #for displaying on the map:
    #longitude = models.FloatField()
    #latitude = models.FloatField()
    #TODO: Methode um von Stadtnamen auf longitude + latitude zu kommen



    def __str__(self):
        # Untenstehend eine Möglichkeit mehrere Bearbeiter (Account namen) mit Komma separiert hintereinander zu schreiben
        # a_string = ', '.join([f'a.name'] for a in self.accounts.all())
        return f'Ort: {self.name}'


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=30)

    def __str__(self):
        return f'Category: {self.name}'
