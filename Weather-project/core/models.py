from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): #show the actual city name
        return self.name

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'
        unique_together = ('name', 'user',) #user cannot have twice the same city