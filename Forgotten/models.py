from django.db import models

# Create your models here.
from django.db import models


class Account(models.Model):
    """
    Diese Klasse ist zuständig um später Orte und Accounts zu verbinden.
    """
    place = models.ForeignKey(
        "Places",
        on_delete=models.CASCADE,
        null=True,
        related_name='accounts'
    )

    def __str__(self):
        return self.name


class Places(models.Model):
    """
    Diese Klasse ermöglicht es später Orte mit Eigenschaften anzulegen
    und diese dann in der Datenbank zu speichern.
    """
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
        """
        Untenstehend eine Möglichkeit mehrere Bearbeiter (Account namen)
        mit Komma separiert hintereinander zu schreiben
        # a_string = ', '.join([f'a.name'] for a in self.accounts.all())
        """
        return f'Ort: {self.name}'


class Category(models.Model):
    """ Klasse für den Admin. """
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=30)

    def __str__(self):
        return f'Category: {self.name}'
