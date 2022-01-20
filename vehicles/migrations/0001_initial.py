# Generated by Django 3.2.11 on 2022-01-20 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Samochód',
                'verbose_name_plural': 'Samochody',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicles.car')),
            ],
            options={
                'verbose_name': 'Ocena',
                'verbose_name_plural': 'Oceny',
            },
        ),
    ]