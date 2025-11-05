# 📝 Como Usar o Shell do Django Corretamente

## ⚠️ Problema Comum

Quando você cola comandos no shell do Django, eles precisam ser executados **linha por linha**, não todos juntos em uma única linha.

## ✅ Forma Correta

### Opção 1: Executar Linha por Linha

No shell do Django (`python manage.py shell`), execute cada linha separadamente:

```python
from django.contrib.auth.models import User

email = 'kaiquenunis976@gmail.com'

users = User.objects.filter(email=email)

print(f'Usuários encontrados: {users.count()}')

for u in users:
    print(f'  - ID: {u.id}, Username: {u.username}, Email: {u.email}, Ativo: {u.is_active}, Criado: {u.date_joined}')
```

**Pressione Enter após cada linha!**

### Opção 2: Usar o Script Python

Crie um arquivo `verificar_usuarios_duplicados.py` e execute:

```bash
python manage.py shell < verificar_usuarios_duplicados.py
```

Ou copie o conteúdo do arquivo e cole no shell, linha por linha.

### Opção 3: Executar Comando Único

Para executar um comando simples em uma linha:

```bash
python manage.py shell -c "from django.contrib.auth.models import User; email = 'kaiquenunis976@gmail.com'; users = User.objects.filter(email=email); print(f'Usuários encontrados: {users.count()}'); [print(f'  - ID: {u.id}, Username: {u.username}') for u in users]"
```

## 📋 Exemplos Úteis

### Verificar Usuário Específico

```python
from django.contrib.auth.models import User

email = 'kaiquenunis976@gmail.com'
users = User.objects.filter(email=email)

for u in users:
    print(f'ID: {u.id}, Username: {u.username}, Ativo: {u.is_active}')
```

### Verificar Todos os Emails Duplicados

```python
from django.contrib.auth.models import User
from django.db.models import Count

duplicates = User.objects.values('email').annotate(count=Count('email')).filter(count__gt=1)

for dup in duplicates:
    email = dup['email']
    count = dup['count']
    users = User.objects.filter(email=email)
    print(f'\nEmail: {email} - {count} usuários')
    for u in users:
        print(f'  - ID: {u.id}, Username: {u.username}')
```

### Mesclar Usuários Duplicados

```python
from django.contrib.auth.models import User

email = 'kaiquenunis976@gmail.com'
users = User.objects.filter(email=email).order_by('date_joined')

if users.count() > 1:
    # Manter o mais antigo (primeiro)
    main_user = users.first()
    
    print(f'Usuário principal: ID {main_user.id} - {main_user.username}')
    print(f'Outros usuários: {[u.id for u in users[1:]]}')
    
    # Descomente para deletar os outros (CUIDADO!)
    # for user in users[1:]:
    #     user.delete()
    #     print(f'Usuário {user.id} deletado')
```

## 🎯 Dicas

1. **Pressione Enter após cada linha** quando colar múltiplos comandos
2. **Use `;`** apenas para comandos muito simples na mesma linha
3. **Use scripts Python** para comandos complexos
4. **Use `-c`** para executar comandos simples rapidamente

## ⚠️ Atenção

- Sempre faça backup antes de deletar usuários
- Teste comandos em ambiente de desenvolvimento primeiro
- Verifique os resultados antes de executar operações destrutivas

