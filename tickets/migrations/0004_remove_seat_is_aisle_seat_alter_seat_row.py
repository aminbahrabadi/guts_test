# Generated by Django 4.0 on 2021-12-17 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_alter_seat_unique_together_remove_seat_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='is_aisle_seat',
        ),
        migrations.AlterField(
            model_name='seat',
            name='row',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='tickets.row', verbose_name='Seat Row'),
        ),
    ]
