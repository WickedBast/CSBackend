# Generated by Django 4.0.3 on 2022-03-14 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('MUNICIPALITY', 'Municipality'), ('COOPERATIVE', 'Cooperative')], max_length=20, verbose_name='Types')),
                ('community_name', models.CharField(max_length=30, verbose_name='community name')),
                ('zip_code', models.CharField(max_length=20, verbose_name='zip code')),
                ('phone_number', models.CharField(max_length=20, verbose_name='phone number')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
