# Generated by Django 4.0 on 2021-12-19 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_customer_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='aisle_required',
            field=models.BooleanField(default=False, verbose_name='Need Aisle seat'),
        ),
    ]
