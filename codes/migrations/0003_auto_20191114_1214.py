# Generated by Django 2.2.6 on 2019-11-14 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0002_auto_20191113_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to='images'),
        ),
    ]
