# Generated by Django 4.2.2 on 2023-07-05 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userProfile', '0001_initial'),
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_instructor', to='userProfile.userprofile'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_student', to='userProfile.userprofile'),
        ),
    ]
