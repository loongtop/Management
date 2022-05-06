# Generated by Django 4.0.4 on 2022-05-06 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='permission',
        ),
        migrations.AddField(
            model_name='role',
            name='permission',
            field=models.ManyToManyField(max_length=32, to='rbac.permission', verbose_name='permission'),
        ),
    ]
