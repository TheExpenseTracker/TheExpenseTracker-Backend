# Generated by Django 5.0.1 on 2024-03-05 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_customer_profileimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='age',
            field=models.IntegerField(default=18),
        ),
        migrations.AddField(
            model_name='customer',
            name='location',
            field=models.CharField(default='Ktm , Nepal', max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
