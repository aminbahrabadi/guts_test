# Generated by Django 4.0 on 2021-12-19 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_alter_row_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.section', verbose_name='Section'),
        ),
    ]
