# Generated by Django 4.0 on 2023-08-09 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_alter_user_user_id_votecomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(default='yGEhCcDIfR', max_length=20, unique=True),
        ),
    ]