from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self): #show the actual city name
        return self.name

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'