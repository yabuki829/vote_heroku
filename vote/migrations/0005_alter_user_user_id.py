# Generated by Django 4.0 on 2023-08-10 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(default='oae9H5yexR', max_length=20, unique=True),
        ),
    ]