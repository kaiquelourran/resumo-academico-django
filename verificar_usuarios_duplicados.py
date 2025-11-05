"""
Script para verificar e corrigir usuários duplicados no banco de dados.
Execute com: python manage.py shell < verificar_usuarios_duplicados.py
Ou copie e cole cada bloco no shell do Django.
"""

from django.contrib.auth.models import User

# Verificar usuários duplicados
email = 'kaiquenunis976@gmail.com'
users = User.objects.filter(email=email)

print(f'\n=== USUÁRIOS ENCONTRADOS COM EMAIL: {email} ===')
print(f'Total: {users.count()} usuário(s)\n')

for u in users:
    print(f'  - ID: {u.id}')
    print(f'    Username: {u.username}')
    print(f'    Email: {u.email}')
    print(f'    Ativo: {u.is_active}')
    print(f'    Criado: {u.date_joined}')
    print(f'    Primeiro Nome: {u.first_name}')
    print(f'    Último Nome: {u.last_name}')
    print()

# Verificar todos os emails duplicados no sistema
from django.db.models import Count

print('\n=== TODOS OS EMAILS COM MÚLTIPLOS USUÁRIOS ===')
duplicates = User.objects.values('email').annotate(count=Count('email')).filter(count__gt=1).order_by('-count')

if duplicates.exists():
    print(f'Total de emails com duplicados: {duplicates.count()}\n')
    for dup in duplicates:
        email = dup['email']
        count = dup['count']
        print(f'\nEmail: {email} - {count} usuário(s)')
        users = User.objects.filter(email=email).order_by('date_joined')
        for u in users:
            print(f'  - ID: {u.id}, Username: {u.username}, Ativo: {u.is_active}, Criado: {u.date_joined}')
else:
    print('Nenhum email duplicado encontrado (exceto o caso acima).')

