# Generated by Django 5.1.1 on 2024-10-14 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_rename_editor_id_article_editor_and_more'),
        ('landing_page', '0001_initial'),
        ('user_authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_comments', to='user_authentication.userprofile'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='article_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_published',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
