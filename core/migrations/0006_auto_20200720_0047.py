# Generated by Django 3.0.8 on 2020-07-20 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200719_2150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='total_price',
        ),
    ]
