# Generated by Django 2.2.2 on 2019-06-08 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xfzauth', '0002_auto_20190607_1436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='date_joined',
            new_name='data_joined',
        ),
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
