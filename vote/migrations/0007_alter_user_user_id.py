# Generated by Django 4.0 on 2023-08-21 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0006_vote_pv_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(default='VH3owuPUbZ', max_length=20, unique=True),
        ),
    ]
