# Generated by Django 2.1.7 on 2019-03-09 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('milliard', '0006_auto_20190309_1452'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together={('question', 'choice_text')},
        ),
    ]