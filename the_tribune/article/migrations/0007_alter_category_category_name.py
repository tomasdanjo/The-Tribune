# Generated by Django 5.1.3 on 2024-12-03 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_alter_category_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(choices=[('news', 'News'), ('sports', 'Sports'), ('religion', 'Religion'), ('entertainment', 'Entertainment'), ('technology', 'Technology'), ('lifestyle', 'Lifestyle'), ('opinion', 'Opinion'), ('editorial', 'Editorial'), ('featured_topics', 'Featured Topics'), ('environment', 'Environment'), ('sci_and_tech', 'Science & Tech.')], default='news', max_length=100),
        ),
    ]