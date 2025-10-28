# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questoes', '0003_adicionar_campos_concurso'),
    ]

    operations = [
        # Renomear 'tipo' para 'tipo_problema'
        migrations.RenameField(
            model_name='relatoriobug',
            old_name='tipo',
            new_name='tipo_problema',
        ),
        
        # Alterar choices do tipo_problema
        migrations.AlterField(
            model_name='relatoriobug',
            name='tipo_problema',
            field=models.CharField(choices=[('bug', 'Bug'), ('melhoria', 'Melhoria'), ('duvida', 'Dúvida'), ('outro', 'Outro')], default='bug', max_length=20, verbose_name='Tipo de Problema'),
        ),
        
        # Adicionar campos novos
        migrations.AddField(
            model_name='relatoriobug',
            name='nome_usuario',
            field=models.CharField(default='', max_length=200, verbose_name='Nome do Usuário'),
        ),
        migrations.AddField(
            model_name='relatoriobug',
            name='email_usuario',
            field=models.EmailField(default='', max_length=254, verbose_name='E-mail do Usuário'),
        ),
        migrations.AddField(
            model_name='relatoriobug',
            name='pagina_erro',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Página do Erro'),
        ),
        
        # Alterar id_usuario para SET_NULL
        migrations.AlterField(
            model_name='relatoriobug',
            name='id_usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]

