# Generated by Django 4.1.4 on 2023-01-25 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_comparisonimage_ret'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, default='ๅ็กใ', max_length=32, null=True),
        ),
    ]
