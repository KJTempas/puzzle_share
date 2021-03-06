# Generated by Django 3.1.5 on 2021-01-21 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzle_share', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puzzle',
            name='checked_out',
        ),
        migrations.AddField(
            model_name='puzzle',
            name='pieces',
            field=models.PositiveSmallIntegerField(choices=[(50, '50 pieces or less'), (100, '100 pieces'), (250, '250 pieces'), (500, '500 pieces'), (750, '750 pieces'), (1000, '1000 pieces')], default=500),
        ),
        migrations.AddField(
            model_name='puzzle',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Available to borrow'), (2, 'Borrowed by someone')], default=1),
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='company',
            field=models.CharField(help_text='Enter name of puzzle manufacturer', max_length=20),
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='name',
            field=models.CharField(help_text='Enter brief description of puzzle picture or name of puzzle', max_length=20),
        ),
    ]
