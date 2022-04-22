# Generated by Django 4.0.4 on 2022-04-22 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0002_alter_partner_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='type',
            field=models.CharField(blank=True, choices=[('LOCAL', 'Local'), ('CLEANSTOCK', 'CleanStock')], max_length=30, null=True, verbose_name='Types'),
        ),
    ]
