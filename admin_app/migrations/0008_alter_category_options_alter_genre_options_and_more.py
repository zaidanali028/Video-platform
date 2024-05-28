# Generated by Django 5.0.6 on 2024-05-24 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0007_alter_category_status_alter_video_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-updated_at', 'created_at']},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['-updated_at', 'created_at']},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-updated_at', 'created_at']},
        ),
        migrations.AddField(
            model_name='video',
            name='thumb_image_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
