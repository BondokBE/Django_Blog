# Generated by Django 2.1.5 on 2019-02-23 12:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateField(default=datetime.datetime(2019, 2, 23, 12, 45, 17, 587833, tzinfo=utc)),
        ),
    ]