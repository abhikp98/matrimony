# Generated by Django 5.0.3 on 2024-05-31 10:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_userprofile_avatar_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(default=datetime.date.today, max_length=8),
        ),
    ]