# Generated by Django 4.0.4 on 2022-05-27 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='dob',
            field=models.DateField(),
        ),
    ]