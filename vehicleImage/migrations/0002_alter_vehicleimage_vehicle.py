# Generated by Django 4.2.2 on 2023-07-06 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0001_initial'),
        ('vehicleImage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleimage',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_image', to='vehicle.vehicle'),
        ),
    ]