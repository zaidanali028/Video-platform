# Generated by Django 5.0.6 on 2024-06-09 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0006_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='brand_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
