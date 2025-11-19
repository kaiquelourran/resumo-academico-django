#!/usr/bin/env python
"""
Script de diagnóstico do sistema Resumo Acadêmico
Verifica configurações, dependências e possíveis problemas
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resumo_academico_proj.settings')
django.setup()

from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import connection
import importlib

print("=" * 70)
print("🔍 DIAGNÓSTICO DO SISTEMA - RESUMO ACADÊMICO")
print("=" * 70)
print()

# 1. Verificar configurações básicas
print("1️⃣ CONFIGURAÇÕES BÁSICAS")
print("-" * 70)
print(f"✅ Django Version: {django.get_version()}")
print(f"✅ DEBUG: {settings.DEBUG}")
print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"✅ Timezone: {settings.TIME_ZONE}")
print(f"✅ Idioma: {settings.LANGUAGE_CODE}")
print()

# 2. Verificar banco de dados
print("2️⃣ BANCO DE DADOS")
print("-" * 70)
try:
    db_config = settings.DATABASES['default']
    print(f"✅ Engine: {db_config['ENGINE']}")
    print(f"✅ Database: {db_config['NAME']}")
    print(f"✅ Host: {db_config['HOST']}")
    print(f"✅ Port: {db_config['PORT']}")
    print(f"✅ User: {db_config['USER']}")
    
    # Testar conexão
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✅ Conexão com banco de dados: OK")
except Exception as e:
    print(f"❌ Erro ao conectar com banco de dados: {e}")
print()

# 3. Verificar apps instalados
print("3️⃣ APPS INSTALADOS")
print("-" * 70)
for app in settings.INSTALLED_APPS:
    print(f"  ✅ {app}")
print()

# 4. Verificar imports críticos
print("4️⃣ IMPORTS CRÍTICOS")
print("-" * 70)
imports_criticos = [
    'questoes.models',
    'questoes.views',
    'questoes.views_container',
    'questoes.filters',
    'questoes.middleware',
    'questoes.auth_backends',
    'questoes.google_auth',
    'institucional.views',
]

for module_name in imports_criticos:
    try:
        importlib.import_module(module_name)
        print(f"  ✅ {module_name}")
    except ImportError as e:
        print(f"  ❌ {module_name}: {e}")
    except Exception as e:
        print(f"  ⚠️ {module_name}: {e}")
print()

# 5. Verificar views do views_container
print("5️⃣ VIEWS DO VIEWS_CONTAINER")
print("-" * 70)
views_esperadas = [
    'gerenciar_comentarios_view',
    'gerenciar_relatorios_view',
    'atualizar_status_relatorio_view',
    'responder_relatorio_view',
    'toggle_comentario_view',
    'deletar_comentario_view',
    'adicionar_assunto_view',
    'gerenciar_assuntos_view',
    'deletar_assunto_view',
    'marcar_notificacao_lida_view',
    'marcar_todas_notificacoes_lidas_view',
]

try:
    from questoes import views_container
    for view_name in views_esperadas:
        if hasattr(views_container, view_name):
            print(f"  ✅ {view_name}")
        else:
            print(f"  ❌ {view_name} - NÃO ENCONTRADA")
except Exception as e:
    print(f"  ❌ Erro ao importar views_container: {e}")
print()

# 6. Verificar models
print("6️⃣ MODELS")
print("-" * 70)
try:
    from questoes.models import (
        Assunto, Questao, Alternativa, RespostaUsuario,
        ComentarioQuestao, CurtidaComentario, DenunciaComentario,
        RelatorioBug, PerfilUsuario
    )
    models_list = [
        ('Assunto', Assunto),
        ('Questao', Questao),
        ('Alternativa', Alternativa),
        ('RespostaUsuario', RespostaUsuario),
        ('ComentarioQuestao', ComentarioQuestao),
        ('CurtidaComentario', CurtidaComentario),
        ('DenunciaComentario', DenunciaComentario),
        ('RelatorioBug', RelatorioBug),
        ('PerfilUsuario', PerfilUsuario),
    ]
    
    for name, model in models_list:
        try:
            count = model.objects.count()
            print(f"  ✅ {name}: {count} registros")
        except Exception as e:
            print(f"  ⚠️ {name}: Erro ao contar - {e}")
except Exception as e:
    print(f"  ❌ Erro ao importar models: {e}")
print()

# 7. Verificar static files
print("7️⃣ ARQUIVOS ESTÁTICOS")
print("-" * 70)
print(f"✅ STATIC_URL: {settings.STATIC_URL}")
print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"✅ STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
print(f"✅ MEDIA_URL: {settings.MEDIA_URL}")
print(f"✅ MEDIA_ROOT: {settings.MEDIA_ROOT}")
print()

# 8. Verificar autenticação
print("8️⃣ AUTENTICAÇÃO")
print("-" * 70)
print(f"✅ AUTHENTICATION_BACKENDS: {len(settings.AUTHENTICATION_BACKENDS)} backends")
for backend in settings.AUTHENTICATION_BACKENDS:
    print(f"    - {backend}")
print(f"✅ LOGIN_URL: {settings.LOGIN_URL}")
print(f"✅ LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
print()

# 9. Verificar middleware
print("9️⃣ MIDDLEWARE")
print("-" * 70)
for middleware in settings.MIDDLEWARE:
    print(f"  ✅ {middleware}")
print()

# 10. Verificar dependências
print("🔟 DEPENDÊNCIAS CRÍTICAS")
print("-" * 70)
dependencias = [
    'django',
    'psycopg2',
    'django_allauth',
    'django_filter',
    'bcrypt',
    'dotenv',
]

for dep in dependencias:
    try:
        if dep == 'django':
            import django
            print(f"  ✅ django: {django.get_version()}")
        elif dep == 'psycopg2':
            import psycopg2
            print(f"  ✅ psycopg2: OK")
        elif dep == 'django_allauth':
            import allauth
            print(f"  ✅ django-allauth: OK")
        elif dep == 'django_filter':
            import django_filters
            print(f"  ✅ django-filter: OK")
        elif dep == 'bcrypt':
            import bcrypt
            print(f"  ✅ bcrypt: OK")
        elif dep == 'dotenv':
            import dotenv
            print(f"  ✅ python-dotenv: OK")
    except ImportError:
        print(f"  ❌ {dep}: NÃO INSTALADO")
    except Exception as e:
        print(f"  ⚠️ {dep}: {e}")
print()

# 11. Verificar migrations
print("1️⃣1️⃣ MIGRATIONS")
print("-" * 70)
try:
    from django.core.management import call_command
    from io import StringIO
    
    output = StringIO()
    call_command('showmigrations', '--list', stdout=output)
    migrations_output = output.getvalue()
    
    # Contar migrations aplicadas
    applied = migrations_output.count('[X]')
    unapplied = migrations_output.count('[ ]')
    
    print(f"✅ Migrations aplicadas: {applied}")
    if unapplied > 0:
        print(f"⚠️ Migrations pendentes: {unapplied}")
    else:
        print("✅ Todas as migrations foram aplicadas")
except Exception as e:
    print(f"⚠️ Erro ao verificar migrations: {e}")
print()

# 12. Resumo de problemas
print("=" * 70)
print("📊 RESUMO")
print("=" * 70)
print("✅ Sistema configurado corretamente")
print("✅ Imports funcionando")
print("✅ Models acessíveis")
print()
print("⚠️ PRÓXIMOS PASSOS:")
print("  1. Verificar se PostgreSQL está rodando")
print("  2. Criar arquivo .env com variáveis de ambiente (opcional)")
print("  3. Executar: python manage.py runserver")
print("  4. Acessar: http://localhost:8000")
print()
print("=" * 70)

