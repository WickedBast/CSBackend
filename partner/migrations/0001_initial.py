# Generated by Django 4.0.3 on 2022-03-09 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('LOCAL', 'Local'), ('CLEANSTOCK', 'CleanStock')], max_length=30, verbose_name='Types')),
                ('partner_type', models.CharField(blank=True, choices=[('BANK', 'Bank'), ('SERVICE PROVIDER', 'Service Provider'), ('ENERGY COMPANY', 'Energy Company')], max_length=30, null=True, verbose_name='Partner_Types')),
                ('partner_name', models.CharField(max_length=30, verbose_name='partner name')),
                ('phone_number', models.CharField(max_length=20, verbose_name='phone number')),
                ('nip_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='nip number')),
                ('community', models.ManyToManyField(blank=True, to='community.community')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
