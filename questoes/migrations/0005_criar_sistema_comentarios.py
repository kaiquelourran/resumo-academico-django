# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questoes', '0004_atualizar_relatoriobug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComentarioQuestao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_usuario', models.CharField(max_length=150, verbose_name='Nome do Usuário')),
                ('email_usuario', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail do Usuário')),
                ('comentario', models.TextField(verbose_name='Comentário')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('aprovado', models.BooleanField(default=True, verbose_name='Aprovado?')),
                ('reportado', models.BooleanField(default=False, verbose_name='Reportado?')),
                ('data_comentario', models.DateTimeField(auto_now_add=True, verbose_name='Data do Comentário')),
                ('id_comentario_pai', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='questoes.comentarioquestao', verbose_name='Comentário Pai')),
                ('id_questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='questoes.questao', verbose_name='Questão')),
                ('id_usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário (Autenticado)')),
            ],
            options={
                'verbose_name': 'Comentário',
                'verbose_name_plural': 'Comentários',
                'ordering': ['-data_comentario'],
            },
        ),
        migrations.CreateModel(
            name='CurtidaComentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_usuario', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('ip_usuario', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')),
                ('data_curtida', models.DateTimeField(auto_now_add=True, verbose_name='Data da Curtida')),
                ('id_comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curtidas', to='questoes.comentarioquestao', verbose_name='Comentário')),
                ('id_usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Curtida',
                'verbose_name_plural': 'Curtidas',
                'unique_together': {('id_comentario', 'email_usuario')},
                'ordering': ['-data_curtida'],
            },
        ),
        migrations.CreateModel(
            name='DenunciaComentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_usuario', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail do Denunciante')),
                ('ip_usuario', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP do Denunciante')),
                ('motivo', models.TextField(blank=True, null=True, verbose_name='Motivo')),
                ('tipo', models.CharField(blank=True, choices=[('spam', 'Spam'), ('inapropriado', 'Conteúdo Inapropriado'), ('bullying', 'Bullying'), ('outro', 'Outro')], max_length=20, null=True, verbose_name='Tipo')),
                ('data_denuncia', models.DateTimeField(auto_now_add=True, verbose_name='Data da Denúncia')),
                ('id_comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='denuncias', to='questoes.comentarioquestao', verbose_name='Comentário')),
            ],
            options={
                'verbose_name': 'Denúncia',
                'verbose_name_plural': 'Denúncias',
                'ordering': ['-data_denuncia'],
            },
        ),
    ]



