# Generated by Django 5.0.1 on 2024-02-26 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_customer_profileimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profileimg',
            field=models.ImageField(blank=True, default='logo.png', null=True, upload_to=''),
        ),
    ]
