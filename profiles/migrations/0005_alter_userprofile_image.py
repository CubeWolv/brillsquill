# Generated by Django 4.1.4 on 2023-12-18 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_userprofile_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='logo.png', null=True, upload_to='files/'),
        ),
    ]
