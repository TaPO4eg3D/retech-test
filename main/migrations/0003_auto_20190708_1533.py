# Generated by Django 2.2.3 on 2019-07-08 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190708_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='organization',
            field=models.ManyToManyField(blank=True, to='main.Organisation'),
        ),
    ]