# 🔗 URIs de Redirecionamento do Google OAuth - Lista Completa

## ✅ URIs que DEVEM estar configuradas no Google Cloud Console

### 📍 Onde Configurar:
1. Acesse: https://console.cloud.google.com/
2. Vá em: **APIs & Services** > **Credentials**
3. Clique no seu **OAuth 2.0 Client ID**
4. Role até a seção **"Authorized redirect URIs"**
5. Adicione todas as URIs abaixo

---

## 🔴 URIs ANTIGAS (PHP - Manter durante migração)

Estas URIs são do sistema antigo (PHP). Mantenha-as durante a migração para não quebrar o sistema antigo:

1. ✅ `http://localhost:8000/RESUMO%20ACAD%C3%8AMICO/questoes/processar_google_login.php`
2. ✅ `https://resumoacademico.com.br/questoes/processar_google_login.php`

---

## 🔵 URIs NOVAS (Django - django-allauth)

Estas URIs são para o sistema novo (Django) usando django-allauth:

3. ✅ `http://localhost:8000/accounts/google/login/callback/`
4. ✅ `https://resumoacademico.com.br/accounts/google/login/callback/`
5. ✅ `http://127.0.0.1:8000/accounts/google/login/callback/`

---

## 🟢 URIs NOVAS (Django - Biblioteca Oficial Google)

Estas URIs são para o sistema novo (Django) usando a biblioteca oficial do Google (implementação simplificada):

6. ✅ `http://127.0.0.1:8000/questoes/google/callback/` ⬅️ **NOVA - Adicionar esta!**
7. ✅ `http://localhost:8000/questoes/google/callback/` ⬅️ **Adicionar também**
8. ✅ `https://resumoacademico.com.br/questoes/google/callback/` ⬅️ **Para produção**

---

## 📋 Lista Completa para Copiar e Colar

**Cole estas URIs no campo "Authorized redirect URIs" do Google Cloud Console:**

```
http://localhost:8000/RESUMO%20ACAD%C3%8AMICO/questoes/processar_google_login.php
https://resumoacademico.com.br/questoes/processar_google_login.php
http://localhost:8000/accounts/google/login/callback/
https://resumoacademico.com.br/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/google/login/callback/
http://127.0.0.1:8000/questoes/google/callback/
http://localhost:8000/questoes/google/callback/
https://resumoacademico.com.br/questoes/google/callback/
```

**Total: 8 URIs**

---

## ⚠️ Importante

1. **Uma URI por linha** no Google Cloud Console
2. **Inclua a barra final** (`/`) nas URIs do Django
3. **Mantenha as URIs PHP** se ainda usar o sistema antigo
4. **Remova as URIs PHP** apenas depois que o Django estiver 100% em produção
5. **As URIs devem ser EXATAMENTE** como mostrado acima (sem espaços extras)

---

## 🎯 Qual URI Usar Agora?

Com a nova implementação simplificada usando a biblioteca oficial do Google:

- **Desenvolvimento Local:** `http://127.0.0.1:8000/questoes/google/callback/`
- **Produção:** `https://resumoacademico.com.br/questoes/google/callback/`

As URIs do django-allauth (`/accounts/google/login/callback/`) ainda funcionam se você quiser usar o allauth, mas a nova implementação usa `/questoes/google/callback/`.

---

## ✅ Verificação Final

Após adicionar todas as URIs, você deve ter **8 URIs** no total no Google Cloud Console.

**IMPORTANTE:** Certifique-se de clicar em **"SAVE"** após adicionar todas as URIs!

