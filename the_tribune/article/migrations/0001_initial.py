# Generated by Django 5.1.1 on 2024-10-14 12:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='article_photos/')),
                ('caption', models.CharField(max_length=200)),
                ('date_taken', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField()),
                ('status', models.CharField(max_length=100)),
                ('date_published', models.DateTimeField()),
                ('editor_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='editor_id', to='user_authentication.userprofile')),
                ('writer_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='writer_id', to='user_authentication.userprofile')),
                ('photo_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='article.photo')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='article.tag')),
            ],
        ),
    ]
