# Generated by Django 5.1.1 on 2024-09-23 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_dark',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='selected_theme',
            field=models.CharField(default='light', max_length=25),
            preserve_default=False,
        ),
    ]
