# Generated by Django 5.0.1 on 2024-03-14 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineRestaurant', '0003_rename_customer_id_user_info_table_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_id',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]
