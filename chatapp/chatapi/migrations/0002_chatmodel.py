# Generated by Django 4.1.4 on 2022-12-26 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatID', models.IntegerField()),
                ('recieverID', models.IntegerField()),
                ('transmitterID', models.IntegerField()),
                ('content', models.TextField()),
                ('datetime', models.CharField(max_length=32)),
            ],
        ),
    ]
