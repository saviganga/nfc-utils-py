# Generated by Django 3.2.9 on 2023-06-15 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vcf', '0004_auto_20230615_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinformation',
            name='picture',
        ),
    ]
