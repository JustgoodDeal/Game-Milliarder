# Generated by Django 2.1.7 on 2019-03-11 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milliard', '0011_auto_20190310_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
