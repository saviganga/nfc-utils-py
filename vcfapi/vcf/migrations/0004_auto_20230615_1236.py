# Generated by Django 3.2.9 on 2023-06-15 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcf', '0003_userinformation_vcarf_file_path'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinformation',
            options={'ordering': ['-added_on']},
        ),
        migrations.AddField(
            model_name='userinformation',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
