# Generated by Django 5.0.6 on 2024-05-24 18:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminBD', '0003_alter_habitat_cardumen_alter_habitat_zona'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardumen',
            name='id',
        ),
        migrations.AlterField(
            model_name='cardumen',
            name='nombre',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='habitat',
            name='cardumen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminBD.cardumen'),
        ),
        migrations.AlterField(
            model_name='habitat',
            name='zona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminBD.zona'),
        ),
        migrations.AddConstraint(
            model_name='habitat',
            constraint=models.UniqueConstraint(fields=('cardumen', 'zona'), name='composite_primary_key'),
        ),
    ]
