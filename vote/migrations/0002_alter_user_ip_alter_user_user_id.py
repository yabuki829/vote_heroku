# Generated by Django 4.1 on 2023-07-29 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(default='f66uK3XkOy', max_length=20, unique=True),
        ),
    ]
