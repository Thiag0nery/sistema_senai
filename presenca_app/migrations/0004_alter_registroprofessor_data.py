# Generated by Django 4.2.9 on 2024-01-12 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presenca_app', '0003_registroprofessor_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroprofessor',
            name='data',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
