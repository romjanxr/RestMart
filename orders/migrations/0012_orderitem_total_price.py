# Generated by Django 5.1.5 on 2025-02-04 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_orderitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=12),
            preserve_default=False,
        ),
    ]
