from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    cityName = models.CharField(max_length=85)
    #longest city in the word has 85 characthers
    cityId = models.CharField(max_length=25)
    country = models.CharField(max_length=50)
    #longest country in the word has 50 characthers
    countryId = models.CharField(max_length=25)
    urlPath = models.CharField(max_length=250)
    region = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): #show the actual city name
        return (self.cityName + " - " + self.countryId)

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'
        unique_together = ('cityId', 'user',) #user cannot have twice the same city