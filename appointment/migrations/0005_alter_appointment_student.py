# Generated by Django 4.2.2 on 2023-07-11 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0002_alter_userprofile_driving_school'),
        ('appointment', '0004_appointment_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_student', to='userProfile.userprofile'),
        ),
    ]
