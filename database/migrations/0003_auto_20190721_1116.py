# Generated by Django 2.2.1 on 2019-07-21 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20190707_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blogData',
            field=models.TextField(max_length=2000),
        ),
    ]