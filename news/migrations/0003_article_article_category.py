# Generated by Django 4.2.1 on 2023-06-21 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_article_file_content_article_head_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_category',
            field=models.CharField(choices=[('VOICE', 'Voice'), ('TALK', 'Talk'), ('TALE', 'Tale'), ('SONG', 'Song'), ('PHOTO', 'Photo'), ('VIDEO', 'Video')], default='VOICE', max_length=5),
        ),
    ]
