# 📧 Política de Email Único no Sistema

## ✅ Objetivo

Garantir que **cada email seja único** no sistema, independentemente de como o usuário se cadastrou:
- Cadastro manual (formulário)
- Cadastro com Google OAuth

## 🔒 Regras Implementadas

### 1. Cadastro Manual (`cadastro_view`)

**Antes de criar um novo usuário:**
- ✅ Verifica se o email já existe no sistema
- ✅ Se existir, **NÃO permite criar** novo usuário
- ✅ Exibe mensagem: "Este e-mail já está cadastrado no sistema. Por favor, faça login."
- ✅ Sugere usar "Continuar com Google" se o usuário se cadastrou com Google

**Código:**
```python
existing_users = User.objects.filter(email=email)

if existing_users.exists():
    messages.error(request, 'Este e-mail já está cadastrado no sistema. Por favor, faça login.')
    messages.info(request, 'Se você se cadastrou com Google, use o botão "Continuar com Google" para fazer login.')
    return render(request, 'questoes/cadastro.html')
```

### 2. Login com Google (`google_auth.py`)

**Antes de criar um novo usuário:**
- ✅ Verifica se o email já existe no sistema
- ✅ Se existir, **faz login no usuário existente** (não cria novo)
- ✅ Usa o usuário mais antigo se houver múltiplos (caso de migração)
- ✅ Prioriza usuários ativos
- ✅ Atualiza informações do usuário (nome, etc.) se necessário

**Se não existir:**
- ✅ Cria novo usuário
- ✅ Verifica se o username já existe e ajusta se necessário

**Código:**
```python
existing_users = User.objects.filter(email=email).order_by('date_joined')

if existing_users.exists():
    # Usa usuário existente (faz login)
    user = existing_users.filter(is_active=True).first()
    if not user:
        user = existing_users.first()
    created = False
else:
    # Cria novo usuário
    user = User.objects.create(...)
    created = True
```

## 📋 Fluxo de Funcionamento

### Cenário 1: Cadastro Manual Primeiro
1. Usuário se cadastra manualmente com `email@example.com`
2. Usuário tenta se cadastrar novamente com o mesmo email
   - ❌ **BLOQUEADO**: "Este e-mail já está cadastrado"
3. Usuário faz login com Google usando `email@example.com`
   - ✅ **PERMITIDO**: Faz login no usuário existente (não cria novo)

### Cenário 2: Cadastro Google Primeiro
1. Usuário se cadastra com Google usando `email@example.com`
2. Usuário tenta se cadastrar manualmente com o mesmo email
   - ❌ **BLOQUEADO**: "Este e-mail já está cadastrado"
3. Usuário faz login com Google novamente
   - ✅ **PERMITIDO**: Faz login no usuário existente (não cria novo)

### Cenário 3: Novo Usuário
1. Email `email@example.com` não existe no sistema
2. Usuário se cadastra manualmente OU com Google
   - ✅ **PERMITIDO**: Cria novo usuário
3. Próximas tentativas de cadastro com o mesmo email
   - ❌ **BLOQUEADO**: "Este e-mail já está cadastrado"

## 🔧 Tratamento de Casos Especiais

### Múltiplos Usuários com Mesmo Email (Migração)

Se houver múltiplos usuários com o mesmo email (caso de migração do PHP):
- ✅ Usa o usuário **mais antigo** (primeiro criado)
- ✅ Prioriza usuários **ativos**
- ✅ Loga aviso no sistema sobre múltiplos usuários
- ✅ Não cria novo usuário

## 📝 Mensagens ao Usuário

### Cadastro Manual - Email Já Existe
```
❌ Este e-mail já está cadastrado no sistema. Por favor, faça login.
ℹ️ Se você se cadastrou com Google, use o botão "Continuar com Google" para fazer login.
```

### Login Google - Conta Existente
```
✅ Bem-vindo(a) de volta, [Nome]!
```

### Login Google - Novo Cadastro
```
✅ Bem-vindo(a), [Nome]! Cadastro realizado com sucesso.
```

## 🎯 Benefícios

1. **Evita Duplicatas**: Cada email só pode ter um usuário
2. **Flexibilidade**: Usuário pode fazer login com Google mesmo tendo cadastro manual
3. **Segurança**: Evita criação de contas duplicadas
4. **Experiência do Usuário**: Mensagens claras sobre o que fazer

## 🔍 Verificar Email Duplicados

Para verificar se há emails duplicados no sistema:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from django.db.models import Count

# Encontrar emails duplicados
duplicates = User.objects.values('email').annotate(count=Count('email')).filter(count__gt=1)

for dup in duplicates:
    email = dup['email']
    count = dup['count']
    users = User.objects.filter(email=email).order_by('date_joined')
    print(f'\nEmail: {email} - {count} usuários')
    for u in users:
        print(f'  - ID: {u.id}, Username: {u.username}, Criado: {u.date_joined}')
```

## ✅ Status

- ✅ Cadastro manual verifica email duplicado
- ✅ Login Google verifica email duplicado
- ✅ Login Google faz login em conta existente (não cria novo)
- ✅ Mensagens claras para o usuário
- ✅ Tratamento de múltiplos usuários (caso de migração)

