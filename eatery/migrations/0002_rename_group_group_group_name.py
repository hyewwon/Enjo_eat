# Generated by Django 3.2.5 on 2022-10-07 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatery', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='group',
            new_name='group_name',
        ),
    ]
