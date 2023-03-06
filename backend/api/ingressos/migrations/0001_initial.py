# Generated by Django 4.1.7 on 2023-03-06 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomeCompleto', models.CharField(max_length=200)),
                ('nascimento', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organizador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomeCompleto', models.CharField(max_length=200)),
                ('nascimento', models.DateField()),
                ('instagram', models.CharField(blank=True, max_length=100, null=True)),
                ('cpf', models.CharField(blank=True, max_length=11, null=True)),
                ('rg', models.CharField(blank=True, max_length=9, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Organizadores',
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=300)),
                ('descricao', models.TextField()),
                ('data', models.DateTimeField()),
                ('valorIngresso', models.FloatField()),
                ('ingressoTotal', models.IntegerField()),
                ('ingressoDisponivel', models.IntegerField()),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ingressos.categoria')),
                ('organizador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ingressos.organizador')),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtdIngresso', models.IntegerField()),
                ('valorTotal', models.FloatField()),
                ('data', models.DateTimeField()),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ingressos.cliente')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingressos.evento')),
            ],
        ),
    ]
