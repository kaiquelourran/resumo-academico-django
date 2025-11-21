# 🔐 Lógica de Criação e Hash de Senhas - Resumo Acadêmico

## 📋 Resumo Executivo

O projeto usa **Django** para criar e gerenciar senhas, com suporte a **senhas antigas do PHP (bcrypt)** para compatibilidade.

---

## 🔑 Algoritmo de Hash Padrão

### **PBKDF2-SHA256** (Padrão do Django)

**Algoritmo usado para novas senhas:**
- **Nome:** `pbkdf2_sha256`
- **Classe:** `PBKDF2PasswordHasher`
- **Iterações:** 600.000 (padrão Django 4.2)
- **Formato do hash:** `pbkdf2_sha256$600000$salt$hash`

**Exemplo de hash gerado:**
```
pbkdf2_sha256$600000$vMCRpkPuoHk9B15WsxFOck$uEDx6R...
```

**Características:**
- ✅ Seguro e recomendado pelo Django
- ✅ Resistente a ataques de força bruta
- ✅ Usa salt único para cada senha
- ✅ 600.000 iterações (muito seguro)

---

## 💻 Código de Criação de Senha

### 1. **Cadastro de Novo Usuário**

**Localização:** `questoes/views.py` - função `cadastro_view()`

```python
# Linha 1123-1128
user = User.objects.create_user(
    username=username, 
    email=email,
    password=password,  # ← Senha em texto plano (será hasheada automaticamente)
    first_name=nome[:30]
)
```

**O que acontece:**
- `User.objects.create_user()` recebe a senha em texto plano
- Django **automaticamente** faz o hash usando `PBKDF2-SHA256`
- A senha **NUNCA** é armazenada em texto plano no banco
- O hash é salvo no campo `password` da tabela `auth_user`

---

### 2. **Alteração de Senha**

**Localização:** `questoes/views.py` - função `alterar_senha_view()`

```python
# Linha 2887
request.user.set_password(senha_nova)  # ← Hash automático
request.user.save()
```

**O que acontece:**
- `set_password()` faz o hash automaticamente
- Usa o mesmo algoritmo (PBKDF2-SHA256)
- Gera novo salt para a nova senha

---

### 3. **Verificação de Senha**

**Localização:** `questoes/views.py` - função `alterar_senha_view()`

```python
# Linha 2878
from django.contrib.auth.hashers import check_password

if not check_password(senha_atual, request.user.password):
    messages.error(request, 'Senha atual incorreta.')
```

**O que acontece:**
- `check_password()` compara a senha em texto plano com o hash
- Detecta automaticamente o algoritmo usado (PBKDF2 ou bcrypt)
- Retorna `True` se a senha estiver correta

---

## 🔄 Compatibilidade com PHP (bcrypt)

### Backend Customizado

**Localização:** `questoes/auth_backends.py` - classe `PHPPasswordBackend`

**Funcionalidade:**
- Suporta senhas antigas do sistema PHP
- Detecta hashes bcrypt (formato `$2y$`, `$2b$`, `$2a$`)
- Converte `$2y$` (PHP) para `$2b$` (Python bcrypt)
- Permite login de usuários migrados do PHP

**Código:**
```python
# Verifica se a senha é um hash do PHP (bcrypt)
if user.password.startswith('$2y$') or user.password.startswith('$2b$'):
    # Hash do PHP - usar bcrypt
    password_bytes = password.encode('utf-8')
    hash_to_check = user.password.replace('$2y$', '$2b$').encode('utf-8')
    
    if bcrypt.checkpw(password_bytes, hash_to_check):
        return user
else:
    # Hash do Django - usar método padrão
    if user.check_password(password):
        return user
```

---

## 📊 Fluxo Completo de Criação de Senha

### **Cadastro de Novo Usuário:**

```
1. Usuário preenche formulário
   ↓
2. POST para /questoes/cadastro/
   ↓
3. Validações:
   - Nome, email, senha preenchidos
   - Email válido
   - Senha com mínimo 6 caracteres
   ↓
4. User.objects.create_user(
     username=email,
     email=email,
     password=senha_texto_plano  ← Entra em texto plano
   )
   ↓
5. Django internamente:
   - make_password(senha_texto_plano)
   - Gera salt aleatório
   - Aplica PBKDF2-SHA256 (600.000 iterações)
   - Salva hash no banco: pbkdf2_sha256$600000$salt$hash
   ↓
6. Usuário criado com senha hasheada
```

---

## 🔐 Algoritmos Suportados

### **1. PBKDF2-SHA256** (Padrão - Novos Usuários)
- **Formato:** `pbkdf2_sha256$iterations$salt$hash`
- **Iterações:** 600.000
- **Segurança:** ⭐⭐⭐⭐⭐ (Muito Seguro)
- **Uso:** Todos os novos cadastros Django

### **2. Bcrypt** (Legado - Usuários PHP)
- **Formato:** `$2y$rounds$salt$hash` ou `$2b$rounds$salt$hash`
- **Rounds:** 10-12 (padrão)
- **Segurança:** ⭐⭐⭐⭐ (Seguro)
- **Uso:** Usuários migrados do sistema PHP antigo

---

## 📝 Validações de Senha

**Localização:** `resumo_academico_proj/settings.py` - linhas 160-173

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # Verifica se senha é similar ao nome/email
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # Mínimo de caracteres (padrão: 8, mas código usa 6)
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # Bloqueia senhas comuns (ex: "password123")
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # Exige pelo menos 1 número
    },
]
```

**Validação no código:**
```python
# questoes/views.py - linha 1096
elif len(password) < 6:
    messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
```

---

## 🛠️ Como Usar no Código

### **Criar Usuário com Senha:**

```python
from django.contrib.auth.models import User

# Método 1: create_user() - RECOMENDADO (hash automático)
user = User.objects.create_user(
    username='usuario@email.com',
    email='usuario@email.com',
    password='senha123'  # ← Hash automático
)

# Método 2: create() + set_password() (se precisar mais controle)
user = User.objects.create(
    username='usuario@email.com',
    email='usuario@email.com'
)
user.set_password('senha123')  # ← Hash automático
user.save()
```

### **Verificar Senha:**

```python
from django.contrib.auth.hashers import check_password

# Verificar senha em texto plano contra hash
if check_password(senha_texto_plano, user.password):
    print("Senha correta!")
else:
    print("Senha incorreta!")
```

### **Gerar Hash Manualmente:**

```python
from django.contrib.auth.hashers import make_password

# Gerar hash de uma senha
senha_hash = make_password('minhasenha123')
# Retorna: pbkdf2_sha256$600000$salt$hash
```

### **Alterar Senha:**

```python
# Método 1: set_password() - RECOMENDADO
user.set_password('novasenha123')
user.save()

# Método 2: make_password() manual (não recomendado)
from django.contrib.auth.hashers import make_password
user.password = make_password('novasenha123')
user.save()
```

---

## 🔒 Segurança

### **O que o Django faz automaticamente:**

1. ✅ **Hash automático** - Nunca armazena senha em texto plano
2. ✅ **Salt único** - Cada senha tem um salt diferente
3. ✅ **Algoritmo seguro** - PBKDF2-SHA256 com 600.000 iterações
4. ✅ **Validações** - Verifica força da senha antes de salvar
5. ✅ **Proteção contra timing attacks** - Verificação constante de tempo

### **Boas Práticas Implementadas:**

- ✅ Senha mínima de 6 caracteres
- ✅ Validação de email único
- ✅ Hash automático (não precisa fazer manualmente)
- ✅ Suporte a senhas antigas (bcrypt) para migração

---

## 📌 Resumo

### **Para Novos Usuários (Django):**
- **Algoritmo:** PBKDF2-SHA256
- **Iterações:** 600.000
- **Formato:** `pbkdf2_sha256$600000$salt$hash`
- **Criação:** `User.objects.create_user(password='senha')`

### **Para Usuários Antigos (PHP):**
- **Algoritmo:** Bcrypt
- **Formato:** `$2y$rounds$salt$hash` ou `$2b$rounds$salt$hash`
- **Suporte:** Backend customizado `PHPPasswordBackend`

### **Código Recomendado:**
```python
# ✅ CORRETO - Hash automático
user = User.objects.create_user(
    username='email@exemplo.com',
    email='email@exemplo.com',
    password='senha123'  # Django faz hash automaticamente
)

# ✅ CORRETO - Alterar senha
user.set_password('novasenha123')
user.save()

# ✅ CORRETO - Verificar senha
from django.contrib.auth.hashers import check_password
if check_password('senha123', user.password):
    print("Correto!")
```

---

## ⚠️ Importante

1. **NUNCA** armazene senhas em texto plano
2. **SEMPRE** use `create_user()` ou `set_password()` (hash automático)
3. **NUNCA** faça `user.password = 'senha123'` diretamente
4. **SEMPRE** use `check_password()` para verificar senhas
5. **NUNCA** compare senhas diretamente (use `check_password()`)

---

**Data:** 19/11/2025  
**Versão Django:** 4.2.7  
**Status:** ✅ Configurado e funcionando

