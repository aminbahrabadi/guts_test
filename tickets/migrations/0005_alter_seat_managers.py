# Generated by Django 4.0 on 2021-12-17 16:19

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_remove_seat_is_aisle_seat_alter_seat_row'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='seat',
            managers=[
                ('seat', django.db.models.manager.Manager()),
            ],
        ),
    ]
