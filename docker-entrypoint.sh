#!/bin/bash
# Script de inicialização do container Django
# Executa migrations e collectstatic antes de iniciar o servidor

set -e  # Parar em caso de erro

echo "🚀 Iniciando container Django..."

# Aguardar PostgreSQL estar pronto
echo "⏳ Aguardando PostgreSQL estar disponível..."
until python -c "
import sys
import psycopg2
import os

try:
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'resumo_academico_db'),
        user=os.getenv('POSTGRES_USER', 'resumo_user'),
        password=os.getenv('POSTGRES_PASSWORD', 'senha_super_segura_123'),
        host=os.getenv('POSTGRES_HOST', 'db'),
        port=os.getenv('POSTGRES_PORT', '5432')
    )
    conn.close()
    print('✅ PostgreSQL está pronto!')
    sys.exit(0)
except psycopg2.OperationalError:
    print('⏳ PostgreSQL ainda não está pronto, aguardando...')
    sys.exit(1)
" 2>/dev/null; do
  sleep 1
done

echo "✅ PostgreSQL está disponível!"

# Executar migrations
echo "📦 Executando migrations..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear || echo "⚠️  Aviso: collectstatic falhou, continuando..."

# Criar superusuário se não existir (apenas em desenvolvimento)
if [ "$DEBUG" = "True" ]; then
    echo "👤 Verificando superusuário..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("📝 Criando superusuário padrão...")
    User.objects.create_superuser(
        email='admin@resumoacademico.com',
        password='admin123',
        username='admin'
    )
    print("✅ Superusuário criado: admin@resumoacademico.com / admin123")
else:
    print("✅ Superusuário já existe")
EOF
fi

echo "✅ Inicialização concluída!"
echo "🌐 Servidor Django iniciando..."

# Executar comando passado como argumento
exec "$@"

