# 🧪 Como Testar a Página de Login

## ✅ URL Correta

A URL da página de login está correta:
- ✅ `http://127.0.0.1:8000/questoes/login/`
- ✅ `http://localhost:8000/questoes/login/`

Ambas funcionam igualmente!

## 🔧 Solução para ERR_EMPTY_RESPONSE

### 1. Parar o Servidor Django

**No terminal onde o servidor está rodando:**
- Pressione `Ctrl+C` para parar o servidor
- Ou feche o terminal

### 2. Reiniciar o Servidor

```bash
# Ative o ambiente virtual (se necessário)
.\venv\Scripts\activate

# Inicie o servidor
python manage.py runserver
```

**Você deve ver algo como:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 3. Testar a Página

1. Abra o navegador
2. Acesse: `http://127.0.0.1:8000/questoes/login/`
3. Ou: `http://localhost:8000/questoes/login/`

### 4. Verificar se a Página Carrega

A página deve mostrar:
- ✅ Logo "🎓" e título "Resumo Acadêmico"
- ✅ Botões "👤 Usuário Normal" e "👨‍💼 Administrador"
- ✅ Campos de email e senha
- ✅ Botão "Entrar"
- ✅ Separador "OU"
- ✅ Botão "Continuar com Google" (com ícone do Google)

## 🚨 Se Ainda Não Funcionar

### Verificar Erros no Terminal

Olhe o terminal onde o servidor está rodando. Se houver erros, você verá algo como:
```
Error: ...
Exception: ...
```

### Verificar se o Template Existe

```bash
python manage.py check
```

Se houver erros, serão mostrados aqui.

### Testar Outra Página

Tente acessar:
- `http://127.0.0.1:8000/questoes/` - Página inicial
- `http://127.0.0.1:8000/admin/` - Admin do Django

Se essas funcionarem, o problema pode ser específico da página de login.

## 📝 Checklist

- [ ] Servidor Django está rodando
- [ ] Terminal mostra "Starting development server at http://127.0.0.1:8000/"
- [ ] Navegador acessa a URL correta
- [ ] Página de login carrega
- [ ] Botão "Continuar com Google" aparece

## 🔍 URLs para Testar

1. **Página Inicial:** `http://127.0.0.1:8000/questoes/`
2. **Login:** `http://127.0.0.1:8000/questoes/login/`
3. **Cadastro:** `http://127.0.0.1:8000/questoes/cadastro/`
4. **Admin:** `http://127.0.0.1:8000/admin/`

Se todas essas funcionarem, o problema pode ser específico ou temporário.

