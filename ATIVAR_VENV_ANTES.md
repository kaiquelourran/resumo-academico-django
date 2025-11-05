# ⚠️ IMPORTANTE: Ativar o Ambiente Virtual Antes de Executar

## 🔴 Problema

O erro `ModuleNotFoundError: No module named 'google.oauth2'` ocorre quando você não está usando o ambiente virtual (`venv`).

## ✅ Solução

**SEMPRE ative o ambiente virtual antes de executar o Django:**

### Windows PowerShell:
```powershell
# Ativar o ambiente virtual
.\venv\Scripts\Activate.ps1

# Ou se der erro de política:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1

# Depois execute o Django
python manage.py runserver
```

### Windows CMD:
```cmd
# Ativar o ambiente virtual
venv\Scripts\activate.bat

# Depois execute o Django
python manage.py runserver
```

### Linux/Mac:
```bash
# Ativar o ambiente virtual
source venv/bin/activate

# Depois execute o Django
python manage.py runserver
```

## 📋 Verificação

Após ativar o ambiente virtual, você deve ver `(venv)` no início do prompt:

```
(venv) PS C:\Users\Revol\Documents\PLATAFORMA-RESUMO-ACADEMICO>
```

## 🔍 Verificar se as Bibliotecas Estão Instaladas

Após ativar o ambiente virtual, verifique:

```bash
pip list | findstr google
```

Deve mostrar:
```
google-auth==2.41.1
google-auth-httplib2==0.2.1
google-auth-oauthlib==1.2.3
```

## 🛠️ Se Ainda Der Erro

Se mesmo ativando o ambiente virtual ainda der erro, reinstale as bibliotecas:

```bash
# Ativar o ambiente virtual primeiro
.\venv\Scripts\Activate.ps1

# Reinstalar as bibliotecas
pip install -r requirements.txt
```

## ✅ Status

- ✅ Bibliotecas instaladas: `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`
- ✅ Versões atualizadas no `requirements.txt`
- ⚠️ **IMPORTANTE**: Sempre ative o ambiente virtual antes de executar!

