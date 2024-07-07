# Generated by Django 5.0.6 on 2024-06-17 05:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='customer',
        ),
        migrations.AddField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='received_transactions', to='finance.customer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sent_transactions', to='finance.customer'),
            preserve_default=False,
        ),
    ]
