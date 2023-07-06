from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from drivingSchool.models import DrivingSchool
from user.models import User


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print(instance)
    if instance.type == 'I':
        return f'instructor/{instance.email}/{filename}'
    else:
        return f'student/{instance.email}/{filename}'


# Create your models here.
class UserProfile(models.Model):
    TYPE = (
        ('I', 'Instructor'),
        ('S', 'Student')
    )

    COUNTRY = (
        ('CH', 'Switzerland'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('IT', 'Italy')
    )

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Non-Binary')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', null=True)
    email = models.CharField(max_length=254, default='')
    gender = models.CharField(max_length=1, choices=GENDER, null=True)
    type = models.CharField(max_length=1, choices=TYPE, null=True)
    address = models.CharField(max_length=254, default='')
    postal_code = models.CharField(max_length=8, null=True)
    location_city = models.CharField(max_length=254, default='')
    country = models.CharField(max_length=2, choices=COUNTRY, null=True)
    about = models.CharField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    instructor_license = models.CharField(max_length=100, blank=True, null=True)
    driving_school = models.ForeignKey(to=DrivingSchool, on_delete=models.CASCADE, related_name="instructor_profile", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    has_learner_permit = models.BooleanField(default=False, blank=True, null=True)
    phone = models.CharField(max_length=60, default='')
    # available Time --> will be done later
    # packages bought --> will be done later





    def clean(self):
        if self.type == 'I' and not self.instructor_license:
            raise ValidationError({'instructor_license': 'Instructor license is required for instructors.'})

        if self.type == 'S' and self.has_learner_permit is False:
            raise ValidationError({'has_learner_permit': 'Learner permit is required for students'})

        if self.type == 'I' and not self.driving_school:
            raise ValidationError({'driving_school': 'Driving School is required for instructors.'})

    def __str__(self):
        # user_type = dict(self.TYPE)[self.type]
        return f'{self.email}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, email=instance.email)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user.save()
