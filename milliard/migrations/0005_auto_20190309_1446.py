# Generated by Django 2.1.7 on 2019-03-09 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('milliard', '0004_auto_20190309_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='milliard.Question'),
        ),
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together={('question', 'choice_text')},
        ),
    ]
