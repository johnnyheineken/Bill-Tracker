# Generated by Django 2.0 on 2018-01-04 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20180103_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='person',
            name='spendings',
            field=models.FloatField(default=0, verbose_name='spendings'),
        ),
    ]
