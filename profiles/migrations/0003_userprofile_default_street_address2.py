# Generated by Django 3.0.1 on 2023-09-28 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20230928_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='default_street_address2',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
