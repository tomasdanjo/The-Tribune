# Generated by Django 5.1.1 on 2024-10-14 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='editor_id',
            new_name='editor',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='photo_id',
            new_name='photo',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='tag_id',
            new_name='tag',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='writer_id',
            new_name='writer',
        ),
        migrations.AlterField(
            model_name='article',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_published',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
