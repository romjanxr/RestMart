# Generated by Django 5.1.5 on 2025-02-03 09:27

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
