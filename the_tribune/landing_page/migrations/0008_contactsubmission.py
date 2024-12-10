# Generated by Django 5.1.1 on 2024-12-09 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0007_comment_disliked_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]