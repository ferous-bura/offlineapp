# Generated by Django 5.0.6 on 2025-02-09 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_userdevice_userlocation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserDevice',
        ),
    ]
