# Generated by Django 4.0.4 on 2022-05-06 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='nickname',
            field=models.CharField(max_length=32, verbose_name='Nickname'),
        ),
    ]
