# Generated by Django 5.0.6 on 2024-06-08 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0004_alter_video_options_user_brand_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_image_url',
        ),
    ]