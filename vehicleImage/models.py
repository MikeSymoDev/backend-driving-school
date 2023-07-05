from django.db import models

from vehicle.models import Vehicle


def vehicle_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print(instance)
    return f'{instance.id}/{filename}'


# Create your models here.
class VehicleImage(models.Model):
    image = models.ImageField(upload_to=vehicle_image_directory_path, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    vehicle = models.ForeignKey(to=Vehicle, on_delete=models.CASCADE, null=True)
