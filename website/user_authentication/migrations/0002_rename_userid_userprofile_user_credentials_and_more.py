# Generated by Django 5.1.1 on 2024-10-01 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='userID',
            new_name='user_credentials',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
    ]
