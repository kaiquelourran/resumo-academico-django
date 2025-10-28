# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questoes', '0002_relatoriobug'),
    ]

    operations = [
        migrations.AddField(
            model_name='assunto',
            name='concurso_ano',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Ano do Concurso'),
        ),
        migrations.AddField(
            model_name='assunto',
            name='concurso_banca',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Banca'),
        ),
        migrations.AddField(
            model_name='assunto',
            name='concurso_orgao',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Órgão'),
        ),
        migrations.AddField(
            model_name='assunto',
            name='concurso_prova',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Tipo de Prova'),
        ),
    ]



