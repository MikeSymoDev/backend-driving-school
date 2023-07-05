from django.db import models

from vehicle.models import Vehicle


# Create your models here.
class VehicleImage(models.Model):
    image = models.ImageField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    vehicle = models.ForeignKey(to=Vehicle, on_delete=models.CASCADE, null=True)
