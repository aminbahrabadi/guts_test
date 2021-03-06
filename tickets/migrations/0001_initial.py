# Generated by Django 4.0 on 2021-12-17 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserve_name', models.CharField(max_length=255, null=True, verbose_name='Reserve Name')),
                ('size_of_group', models.IntegerField(default=1, verbose_name='Size of Group')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('is_curved', models.BooleanField(default=False, verbose_name='Section is Curved')),
            ],
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Row Name')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Row Order')),
                ('number_of_seats', models.IntegerField(default=1, verbose_name='Number of Seats')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField(null=True, verbose_name='Seat Number')),
                ('rank', models.PositiveSmallIntegerField(choices=[(1, '1st rank'), (2, '2nd rank'), (3, '3rd rank')], default=1, verbose_name='Rank')),
                ('is_aisle_seat', models.BooleanField(default=False, verbose_name='Seat is an Aisle Seat')),
                ('is_front_seat', models.BooleanField(default=False, verbose_name='Seat is a Front Seat')),
                ('is_high_seat', models.BooleanField(default=False, verbose_name='Seat is a High Seat')),
                ('is_blocked', models.BooleanField(default=False, verbose_name='Seat is Blocked')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets.customer', verbose_name='Customer Reserved')),
                ('row', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.row', verbose_name='Seat Row')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.section', verbose_name='Section')),
            ],
            options={
                'unique_together': {('section', 'row', 'seat_number')},
            },
        ),
    ]
