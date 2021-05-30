# Generated by Django 3.2.3 on 2021-05-30 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SavedChat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ws_group_name', models.CharField(max_length=50)),
                ('timestamp_start', models.DateTimeField(auto_now_add=True)),
                ('timestamp_end', models.DateTimeField(auto_now=True)),
                ('chat_data', models.TextField(blank=True)),
                ('supervisor_role', models.CharField(default='nosupervisor', max_length=50)),
            ],
        ),
    ]