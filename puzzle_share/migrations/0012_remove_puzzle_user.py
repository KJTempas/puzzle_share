# Generated by Django 3.1.5 on 2021-03-11 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puzzle_share', '0011_puzzle_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puzzle',
            name='user',
        ),
    ]
