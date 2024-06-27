from django.db import models

# Create your models here.
from django.db import models


# Für das spätere verbinden von Orten zu Accounts
class Account(models.Model):
    Places = models.ForeignKey(
        "Places",
        on_delete=models.CASCADE,
    )


    def __str__(self):
        return self.name


#Places model für die ansicht von Orten
class Places(models.Model):
    class Meta:
        verbose_name_plural = 'Places'

    name = models.CharField(max_length=30)
    story_field = models.TextField(blank=True)
    upload_picture = models.ImageField(null="True", blank="True", upload_to='media/')
    location_map = models.CharField(max_length=40)
    ctime = models.DateTimeField(auto_now_add=True)
    uptime = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


    def __str__(self):
        # Untenstehend eine Möglichkeit mehrere Bearbeiter (Account namen) mit Komma separiert hintereinander zu schreiben
        # a_string = ', '.join([f'a.name'] for a in self.accounts.all())
        return f'Ort: {self.name}'

#Admin
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=30)

    def __str__(self):
        return f'Category: {self.name}'
