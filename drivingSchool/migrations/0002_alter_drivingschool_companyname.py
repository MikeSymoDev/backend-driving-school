# Generated by Django 4.2.2 on 2023-07-06 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivingSchool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drivingschool',
            name='companyName',
            field=models.CharField(max_length=254, null=True, unique=True),
        ),
    ]
