# Generated by Django 3.0.5 on 2021-03-22 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20210322_1920'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='Profile',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='description',
            new_name='bio',
        ),
    ]