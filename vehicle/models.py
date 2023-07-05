from django.core.validators import MinLengthValidator
from django.db import models

from userProfile.models import UserProfile

TRANSMISSION = (
    ('A', 'Automatic'),
    ('M', 'Manual')
)

FUEL_TYPE = (
    ('D', 'Diesel'),
    ('G', 'Gasoline'),
    ('H', 'Hybrid'),
    ('E', 'Electric')
)


# Create your models here.
class Vehicle(models.Model):
    make = models.CharField(max_length=256, null=True)
    model = models.CharField(max_length=256, null=True)
    year = models.CharField(max_length=4, validators=[MinLengthValidator(4)], null=True)
    driving_instructor = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='vehicle')
    transmission = models.CharField(max_length=1, choices=TRANSMISSION, null=True)
    fuel_type = models.CharField(max_length=1, choices=FUEL_TYPE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)