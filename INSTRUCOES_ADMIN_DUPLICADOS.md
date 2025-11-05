# 🗑️ Como Deletar Usuários Duplicados no Django Admin

## 📋 Passo a Passo

### 1. Acessar o Django Admin

1. Execute o servidor Django:
```bash
python manage.py runserver
```

2. Acesse: `http://127.0.0.1:8000/admin/`

3. Faça login com sua conta de administrador

### 2. Verificar Usuários Duplicados

1. No menu lateral, clique em **"Users"** (ou "Usuários")
2. Clique no campo de busca no topo
3. Digite o email duplicado (ex: `kaiquenunis976@gmail.com`)
4. Pressione Enter ou clique em "Search"

### 3. Verificar Dados Associados

Antes de deletar, verifique qual usuário tem mais dados:

**Execute o script:**
```bash
python manage.py shell < verificar_dados_usuario.py
```

Ou copie e cole no shell do Django:
```python
from django.contrib.auth.models import User
from questoes.models import RespostaUsuario, ComentarioQuestao, RelatorioBug

email = 'kaiquenunis976@gmail.com'
users = User.objects.filter(email=email).order_by('date_joined')

for user in users:
    respostas = RespostaUsuario.objects.filter(id_usuario=user).count()
    comentarios = ComentarioQuestao.objects.filter(id_usuario=user).count()
    relatorios = RelatorioBug.objects.filter(id_usuario=user).count()
    total = respostas + comentarios + relatorios
    
    print(f"ID: {user.id}, Username: {user.username}")
    print(f"  Respostas: {respostas}, Comentários: {comentarios}, Relatórios: {relatorios}")
    print(f"  TOTAL: {total} registros")
    print()
```

### 4. Decidir Qual Usuário Manter

**Regra de Ouro:**
- ✅ **Mantenha o usuário com MAIS dados associados**
- ✅ Se ambos tiverem a mesma quantidade, mantenha o **mais antigo** (primeiro criado)
- ❌ **NUNCA delete o usuário com mais dados!**

### 5. Deletar o Usuário Duplicado

1. No Django Admin, encontre os usuários duplicados
2. **Marque a caixa de seleção** ao lado do usuário que você quer deletar
3. Na parte superior, no dropdown "Action", selecione **"Delete selected users"**
4. Clique em **"Go"**
5. Confirme a exclusão

### 6. Verificar se Deletou Corretamente

Após deletar, verifique:

```python
from django.contrib.auth.models import User

email = 'kaiquenunis976@gmail.com'
users = User.objects.filter(email=email)

print(f"Usuários restantes: {users.count()}")
for u in users:
    print(f"  - ID: {u.id}, Username: {u.username}")
```

Deve mostrar apenas **1 usuário**.

## ⚠️ PRECAUÇÕES IMPORTANTES

### ⚠️ ANTES DE DELETAR:

1. **Verifique dados associados:**
   - Respostas de questões (`RespostaUsuario`)
   - Comentários (`ComentarioQuestao`)
   - Relatórios de bugs (`RelatorioBug`)

2. **Se o usuário tem dados:**
   - ❌ **NÃO DELETE** se o usuário tiver mais dados que o outro
   - ✅ **MANTENHA** o usuário com mais dados

3. **Se ambos têm a mesma quantidade:**
   - ✅ **MANTENHA** o usuário mais antigo (primeiro criado)

### ⚠️ CUIDADO:

- ❌ **NUNCA delete o usuário principal** (o que tem mais dados)
- ❌ **NUNCA delete sem verificar dados associados**
- ✅ **SEMPRE faça backup** antes de deletar (se possível)

## 📊 Exemplo: Caso Atual

### Usuários Encontrados:
- **ID: 6**, Username: `a_chave`, Criado: 2025-11-04 (mais recente)
- **ID: 2**, Username: `kaique`, Criado: 2025-10-26 (mais antigo)

### Recomendação:
1. Verifique qual tem mais dados (respostas, comentários, relatórios)
2. Se o ID 2 tem mais dados → **Mantenha ID 2, delete ID 6**
3. Se o ID 6 tem mais dados → **Mantenha ID 6, delete ID 2**
4. Se ambos têm a mesma quantidade → **Mantenha ID 2** (mais antigo)

## 🔍 Verificar Todos os Duplicados

Para ver todos os emails duplicados no sistema:

```python
from django.contrib.auth.models import User
from django.db.models import Count

duplicates = User.objects.values('email').annotate(count=Count('email')).filter(count__gt=1)

for dup in duplicates:
    email = dup['email']
    count = dup['count']
    users = User.objects.filter(email=email)
    print(f"\nEmail: {email} - {count} usuários")
    for u in users:
        print(f"  - ID: {u.id}, Username: {u.username}, Criado: {u.date_joined}")
```

## ✅ Após Deletar

Após deletar os usuários duplicados:

1. O sistema continuará funcionando normalmente
2. O login com Google usará o usuário restante
3. O cadastro manual não permitirá criar novo usuário com o mesmo email
4. Todos os dados ficarão associados ao usuário mantido

## 🎯 Resumo

1. ✅ Acesse o Django Admin
2. ✅ Encontre os usuários duplicados
3. ✅ Verifique dados associados (use o script)
4. ✅ Mantenha o usuário com mais dados (ou o mais antigo)
5. ✅ Delete o usuário duplicado
6. ✅ Verifique se restou apenas 1 usuário

