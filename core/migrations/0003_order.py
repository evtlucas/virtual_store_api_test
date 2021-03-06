# Generated by Django 3.0.8 on 2020-07-16 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_company_customer_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField()),
                ('ship_date', models.DateField()),
                ('delivery_address', models.CharField(max_length=100)),
                ('delivery_city', models.CharField(max_length=100)),
                ('delivery_state', models.CharField(max_length=2)),
                ('delivery_country', models.CharField(max_length=20)),
                ('delivery_phone_number', models.CharField(max_length=15)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Customer')),
            ],
        ),
    ]
