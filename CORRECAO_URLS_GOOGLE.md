# 🔧 Correção das URLs de Redirecionamento do Google OAuth

## ⚠️ Problema Identificado

As URLs de redirecionamento configuradas no Google Cloud Console estão apontando para o sistema antigo (PHP):

**URLs INCORRETAS (atualmente configuradas):**
- ❌ `http://localhost:8000/RESUMO%20ACAD%C3%8AMICO/questoes/processar_google_login.php`
- ❌ `https://resumoacademico.com.br/questoes/processar_google_login.php`

## ✅ URLs Corretas para Django/django-allauth

Você precisa atualizar as **Authorized redirect URIs** no Google Cloud Console para:

**Para Desenvolvimento:**
- ✅ `http://localhost:8000/accounts/google/login/callback/`

**Para Produção:**
- ✅ `https://resumoacademico.com.br/accounts/google/login/callback/`

## 📝 Passo a Passo para Corrigir

1. **Acesse o Google Cloud Console:**
   - https://console.cloud.google.com/
   - Vá em **APIs & Services** > **Credentials**

2. **Encontre seu OAuth Client ID:**
   - Clique no nome do cliente OAuth que você criou

3. **Atualize as "Authorized redirect URIs":**
   
   **⚠️ IMPORTANTE: Você pode manter ambas as URLs durante a migração!**
   
   **OPÇÃO A - Migração Gradual (Recomendado):**
   - **ADICIONE** as URLs do Django (não remova as PHP ainda):
     - ✅ `http://localhost:8000/accounts/google/login/callback/`
     - ✅ `https://resumoacademico.com.br/accounts/google/login/callback/`
   - **MANTENHA** as URLs PHP (para o site continuar funcionando):
     - ✅ `http://localhost:8000/RESUMO%20ACAD%C3%8AMICO/questoes/processar_google_login.php`
     - ✅ `https://resumoacademico.com.br/questoes/processar_google_login.php`
   
   **OPÇÃO B - Migração Completa (Só depois que Django estiver em produção):**
   - **REMOVA** as URLs antigas (com `.php`)
   - **ADICIONE** apenas as URLs do Django

4. **Mantenha as "Authorized JavaScript origins" como estão:**
   - ✅ `http://localhost:8000` (correto)
   - ✅ `http://localhost` (correto)
   - ✅ `https://resumoacademico.com.br` (correto)

5. **Clique em "Save"** para salvar as alterações

## 🔍 Verificação Final

Após salvar, as configurações devem ficar assim:

**Authorized JavaScript origins:**
```
http://localhost:8000
http://localhost
https://resumoacademico.com.br
```

**Authorized redirect URIs:**
```
http://localhost:8000/accounts/google/login/callback/
https://resumoacademico.com.br/accounts/google/login/callback/
```

## ⚠️ Importante

- As URLs do Django **NÃO** contêm `.php`
- O caminho é `/accounts/google/login/callback/` (não `/questoes/processar_google_login.php`)
- Certifique-se de incluir a barra final (`/`) nas URLs de callback
- Após salvar, pode levar alguns minutos para as mudanças entrarem em vigor

## 🧪 Teste

Após corrigir as URLs:
1. Acesse: `http://localhost:8000/questoes/login/`
2. Clique em "Continuar com Google"
3. Deve redirecionar corretamente para o Google e voltar para a aplicação Django

