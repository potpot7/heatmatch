# Generated by Django 4.1.3 on 2023-01-12 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('q_a', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='a1',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='answer',
            name='a2',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='answer',
            name='a3',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='answer',
            name='a4',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='answer',
            name='a5',
            field=models.BooleanField(default=0),
        ),
    ]
