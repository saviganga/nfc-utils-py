# Generated by Django 3.2.9 on 2023-07-10 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='spotify_auth',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
