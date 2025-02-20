from django.db import models



# Create your models here.
class DrivingSchool(models.Model):
    COUNTRY = (
        ('CH', 'Switzerland'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('IT', 'Italy')
    )

    companyName = models.CharField(max_length=254, null=True, unique=True)
    address = models.CharField(max_length=254, default='')
    postal_code = models.CharField(max_length=8, null=True)
    location_city = models.CharField(max_length=254, default='')
    country = models.CharField(max_length=2, choices=COUNTRY, null=True)


    def __str__(self):
        return f'{self.id}: {self.companyName}, {self.postal_code} {self.location_city} ({self.country})'
