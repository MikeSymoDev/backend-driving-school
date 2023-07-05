# Generated by Django 4.2.2 on 2023-07-05 19:30

from django.db import migrations, models
import django.db.models.deletion
import vehicleImage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=vehicleImage.models.vehicle_image_directory_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicle.vehicle')),
            ],
        ),
    ]
