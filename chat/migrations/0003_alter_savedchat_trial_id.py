# Generated by Django 3.2.3 on 2021-06-25 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_savedchat_trial_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedchat',
            name='trial_id',
            field=models.CharField(blank=True, default='unspecified', max_length=50),
        ),
    ]
