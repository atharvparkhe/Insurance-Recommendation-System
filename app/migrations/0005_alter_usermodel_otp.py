# Generated by Django 4.0.4 on 2022-05-27 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_usermodel_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='otp',
            field=models.IntegerField(default=0),
        ),
    ]