# Generated by Django 4.2.11 on 2024-10-20 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0002_roomallocation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomallocation',
            old_name='room_number',
            new_name='room',
        ),
    ]
