# Generated by Django 5.0.1 on 2024-02-03 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presenca_app', '0007_registroprofessor_turno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroprofessor',
            name='turno',
            field=models.CharField(blank=True, choices=[('MATUTINO', 'Matutino'), ('VESPERTINO', 'Vespertino'), ('NOTURNO', 'Noturno')], max_length=15, null=True),
        ),
    ]