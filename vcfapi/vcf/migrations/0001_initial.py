# Generated by Django 3.2.9 on 2023-06-13 11:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(max_length=15, unique=True, verbose_name='phone number')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email address')),
                ('organisation', models.CharField(blank=True, max_length=50, null=True)),
                ('position', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]