# Generated by Django 3.2.7 on 2021-10-03 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=60, unique=True)),
                ('author', models.CharField(max_length=60)),
                ('price', models.IntegerField()),
                ('copies', models.IntegerField()),
            ],
        ),
    ]
