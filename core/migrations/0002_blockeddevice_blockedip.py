# Generated by Django 5.0.6 on 2025-02-07 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=255, unique=True)),
                ('ip_address', models.CharField(max_length=255)),
                ('user_agent', models.CharField(max_length=255)),
                ('blocked_at', models.DateTimeField(auto_now_add=True)),
                ('blocked_until', models.DateTimeField(blank=True, null=True)),
                ('is_blocked', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlockedIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=255, unique=True)),
                ('blocked_at', models.DateTimeField(auto_now_add=True)),
                ('blocked_until', models.DateTimeField(blank=True, null=True)),
                ('is_blocked', models.BooleanField(default=True)),
            ],
        ),
    ]
