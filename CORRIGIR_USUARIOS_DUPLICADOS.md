# 🔧 Como Corrigir Usuários Duplicados no Banco de Dados

## ⚠️ Problema Identificado

O erro mostra que existem **2 usuários** com o mesmo email `kaiquenunis976@gmail.com`:

```
ERROR: get() returned more than one User -- it returned 2!
django.contrib.auth.models.User.MultipleObjectsReturned
```

## ✅ Solução Aplicada

O código foi corrigido para:
1. **Usar `filter().first()`** ao invés de `get()` para lidar com múltiplos usuários
2. **Priorizar usuários ativos** se houver múltiplos
3. **Usar o primeiro usuário** se não houver ativo
4. **Criar novo usuário** apenas se não existir nenhum

## 🔍 Verificar Usuários Duplicados

Execute este comando para ver todos os usuários com email duplicado:

```bash
python manage.py shell
```

Depois execute:

```python
from django.contrib.auth.models import User
from django.db.models import Count

# Encontrar emails duplicados
duplicates = User.objects.values('email').annotate(count=Count('email')).filter(count__gt=1)
print(f'Emails com múltiplos usuários: {duplicates.count()}')

for dup in duplicates:
    email = dup['email']
    count = dup['count']
    users = User.objects.filter(email=email)
    print(f'\nEmail: {email} - {count} usuários')
    for u in users:
        print(f'  - ID: {u.id}, Username: {u.username}, Ativo: {u.is_active}, Criado: {u.date_joined}')
```

## 🎯 Opções para Corrigir Duplicados

### Opção 1: Manter o Primeiro Usuário (Recomendado)

O código já está configurado para usar o primeiro usuário ativo, ou o primeiro se não houver ativo.

### Opção 2: Mesclar Usuários Duplicados

Se quiser mesclar os dados dos usuários duplicados:

```python
from django.contrib.auth.models import User

# Encontrar usuários duplicados
email = 'kaiquenunis976@gmail.com'
users = User.objects.filter(email=email).order_by('date_joined')

if users.count() > 1:
    # Manter o primeiro (mais antigo)
    main_user = users.first()
    
    # Mesclar dados dos outros usuários
    for user in users[1:]:
        # Transferir dados se necessário
        if not main_user.first_name and user.first_name:
            main_user.first_name = user.first_name
        if not main_user.last_name and user.last_name:
            main_user.last_name = user.last_name
        
        # Deletar usuário duplicado (se quiser)
        # user.delete()  # CUIDADO: Descomente apenas se tiver certeza!
    
    main_user.save()
    print(f'Usuário principal: {main_user.id} - {main_user.email}')
```

### Opção 3: Deletar Usuários Duplicados (Cuidado!)

**⚠️ ATENÇÃO: Só faça isso se tiver certeza!**

```python
from django.contrib.auth.models import User

# Encontrar usuários duplicados
email = 'kaiquenunis976@gmail.com'
users = User.objects.filter(email=email).order_by('date_joined')

if users.count() > 1:
    # Manter o primeiro (mais antigo)
    main_user = users.first()
    
    # Deletar os outros
    for user in users[1:]:
        print(f'Deletando usuário ID: {user.id}')
        user.delete()
    
    print(f'Usuário mantido: {main_user.id} - {main_user.email}')
```

## ✅ Teste

Após a correção, o login com Google deve funcionar corretamente:

1. Execute o servidor Django
2. Tente fazer login com Google
3. O código agora lida com múltiplos usuários automaticamente
4. Você deve ser logado no primeiro usuário encontrado

## 📝 Nota

O código agora está preparado para lidar com usuários duplicados, mas é recomendado corrigir os duplicados no banco de dados para evitar problemas futuros.

