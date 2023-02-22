# Generated by Django 4.1.4 on 2023-01-17 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_gender'),
        ('friend', '0003_remove_friend_followed_friend_followed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='followed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed', to='accounts.profile'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='accounts.profile'),
        ),
    ]
