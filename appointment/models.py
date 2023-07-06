from django.db import models
from rest_framework.exceptions import ValidationError

from userProfile.models import UserProfile

TIME_SLOTS = (
    ('08:00', '8:00 AM'),
    ('09:00', '9:00 AM'),
    ('10:00', '10:00 AM'),
    ('11:00', '11:00 AM'),
    ('12:00', '12:00 PM'),
    ('13:00', '1:00 PM'),
    ('14:00', '2:00 PM'),
    ('15:00', '3:00 PM'),
    ('16:00', '4:00 PM'),
    ('17:00', '5:00 PM'),
    ('18:00', '6:00 PM'),
)


# Create your models here.
class Appointment(models.Model):
    title = models.CharField(max_length=254, default='')
    location = models.CharField(max_length=500, default='')
    instructor = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name="appointment_instructor")
    student = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name="appointment_student")
    notes = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateField(null=True)
    start_slot = models.CharField(max_length=5, choices=TIME_SLOTS)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.instructor and self.instructor.type != 'I':
            raise ValidationError({'instructor': 'Only instructors can be assigned to the instructor field.'})

        if self.student and self.student.type != 'S':
            raise ValidationError({'student': 'Only students can be assigned to the student field.'})

    def __str__(self):
        return f'{self.id}: {self.title}({self.date}: {self.start_slot})'
