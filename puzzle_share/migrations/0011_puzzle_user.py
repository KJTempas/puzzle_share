# Generated by Django 3.1.5 on 2021-03-11 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('puzzle_share', '0010_auto_20210222_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='auth.user'),
            preserve_default=False,
        ),
    ]
