# Generated by Django 5.1.1 on 2024-10-14 12:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0001_initial'),
        ('user_authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_published', models.DateTimeField()),
                ('content', models.TextField()),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='article.article')),
                ('commenter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_authentication.userprofile')),
            ],
        ),
    ]
