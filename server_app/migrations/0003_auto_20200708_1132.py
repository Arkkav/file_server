# Generated by Django 3.0.8 on 2020-07-08 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_app', '0002_file_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='hash',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
