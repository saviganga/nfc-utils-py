# Generated by Django 3.2.9 on 2023-06-13 16:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vcf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='added_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinformation',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
