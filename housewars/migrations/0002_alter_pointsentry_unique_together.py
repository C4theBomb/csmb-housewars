# Generated by Django 4.0.4 on 2022-09-03 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('housewars', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pointsentry',
            unique_together={('activity', 'award')},
        ),
    ]
