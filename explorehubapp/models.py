from django.db import models

class Destinations(models.Model):
    Name=models.CharField(max_length=250)
    CHOICES=[
        (1,'Sunny'),
        (2,'Rainy'),
        (3,'Cloudy'),
        (4,'Cold')
    ]
    Weather = models.IntegerField(choices=CHOICES)
    State = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    Google_Maps_Link = models.URLField(max_length=500, blank=True, null=True)
    explore_img = models.ImageField(upload_to='explore/')
    Description = models.CharField(max_length=5000)
