# 🔧 Solução para ERR_EMPTY_RESPONSE

## ⚠️ Problema

`ERR_EMPTY_RESPONSE` geralmente significa que:
- O servidor Django não está respondendo
- O servidor crashou ou travou
- Há muitas requisições pendentes
- A URL está incorreta

## ✅ Solução Rápida

### 1. Parar o Servidor Django

**Opção A - Via Terminal:**
```bash
# Pressione Ctrl+C no terminal onde o servidor está rodando
```

**Opção B - Forçar Parada:**
```bash
# Windows PowerShell
Get-Process -Name python | Where-Object {$_.Path -like "*venv*"} | Stop-Process -Force

# Ou encontre o PID e mate o processo
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### 2. Limpar Conexões Pendentes

```bash
# Aguarde alguns segundos para conexões TIME_WAIT expirarem
# Ou reinicie o computador se necessário
```

### 3. Reiniciar o Servidor Django

```bash
# Ative o ambiente virtual
.\venv\Scripts\activate

# Execute o servidor
python manage.py runserver
```

### 4. Testar

Acesse: `http://localhost:8000/questoes/login/`

## 🔍 Verificação

### Verificar se o servidor está rodando:

```bash
netstat -ano | findstr :8000
```

Você deve ver algo como:
```
TCP    0.0.0.0:8000           0.0.0.0:0              LISTENING
```

### Verificar se há erros:

```bash
python manage.py check
```

## 🚨 Causas Comuns

1. **Servidor travado:**
   - Muitas requisições simultâneas
   - Erro não tratado na view
   - **Solução:** Reiniciar o servidor

2. **URL incorreta:**
   - Tentando acessar URL que não existe
   - **Solução:** Verificar a URL correta

3. **Erro no código:**
   - View retornando vazio
   - Exception não tratada
   - **Solução:** Verificar logs do servidor

4. **Porta ocupada:**
   - Outro processo usando a porta 8000
   - **Solução:** Matar o processo ou usar outra porta

## 📝 URLs Corretas

### Páginas principais:
- Login: `http://localhost:8000/questoes/login/`
- Cadastro: `http://localhost:8000/questoes/cadastro/`
- Index: `http://localhost:8000/questoes/index/`
- Admin: `http://localhost:8000/admin/`

### Google OAuth (django-allauth):
- Login Google: `http://localhost:8000/accounts/google/login/`
- Callback Google: `http://localhost:8000/accounts/google/login/callback/`

## ✅ Passos para Resolver

1. ✅ **Pare o servidor** (Ctrl+C no terminal)
2. ✅ **Aguarde 10 segundos** (para conexões expirarem)
3. ✅ **Reinicie o servidor**: `python manage.py runserver`
4. ✅ **Teste a URL**: `http://localhost:8000/questoes/login/`
5. ✅ **Verifique os logs** no terminal do servidor

## 🎯 Se Ainda Não Funcionar

1. **Verifique os logs do servidor Django** no terminal
2. **Verifique se há erros** no código
3. **Teste com outra porta**: `python manage.py runserver 8001`
4. **Reinicie o computador** se necessário

