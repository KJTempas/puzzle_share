# Generated by Django 3.1.5 on 2021-02-22 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzle_share', '0009_puzzle_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puzzle',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
