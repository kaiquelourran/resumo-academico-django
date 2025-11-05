# 📋 URLs para Google Cloud Console

## ✅ URLs que você deve colocar em "Authorized JavaScript origins"

### 🔵 Para Desenvolvimento (Local):
```
http://localhost:8000
http://localhost
```

### 🟢 Para Produção (Hostinger):
```
https://resumoacademico.com.br
```

### 📝 Lista Completa para "Authorized JavaScript origins":

```
http://localhost:8000
http://localhost
https://resumoacademico.com.br
```

---

## ✅ URLs que você deve colocar em "Authorized redirect URIs"

### 🔵 Para Desenvolvimento (Local):
```
http://localhost:8000/accounts/google/login/callback/
```

### 🟢 Para Produção (Hostinger):
```
https://resumoacademico.com.br/accounts/google/login/callback/
```

### 🟡 URLs PHP (Manter durante migração - se ainda usar):
```
http://localhost:8000/RESUMO%20ACAD%C3%8AMICO/questoes/processar_google_login.php
https://resumoacademico.com.br/questoes/processar_google_login.php
```

## 📝 Lista Completa para Copiar e Colar

**Cole estas URLs no campo "Authorized redirect URIs" do Google Cloud Console:**

```
http://localhost:8000/accounts/google/login/callback/
https://resumoacademico.com.br/accounts/google/login/callback/
http://localhost:8000/RESUMO%20ACAD%C3%8AMICO/questoes/processar_google_login.php
https://resumoacademico.com.br/questoes/processar_google_login.php
```

## ⚠️ Importante

1. **Uma URL por linha** no Google Cloud Console
2. **Inclua a barra final** (`/`) nas URLs do Django
3. **Mantenha as URLs PHP** se ainda usar o sistema antigo
4. **Remova as URLs PHP** apenas depois que o Django estiver em produção

## 📍 Onde Colocar

1. Acesse: https://console.cloud.google.com/
2. Vá em: **APIs & Services** > **Credentials**
3. Clique no seu **OAuth 2.0 Client ID**
4. Role até a seção **"Authorized redirect URIs"**
5. Clique em **"ADD URI"** para cada URL
6. Cole as URLs uma por uma
7. Clique em **"SAVE"** no final

## ✅ Verificação Final

Após salvar, você deve ter **4 URLs** no total:
- 2 URLs do Django (novas)
- 2 URLs do PHP (antigas - mantenha se ainda usar)

