# 🔧 Corrigir Login com Google - Credenciais Placeholder

## ⚠️ Problema Identificado

A Social Application está configurada com valores **placeholder**, não com as credenciais reais do Google!

**Status atual:**
- ❌ Client ID: `placeholder` (deve ser o Client ID real do Google)
- ❌ Client Secret: `placeholder` (deve ser o Client Secret real do Google)
- ⚠️ Site: `example.com` (deve ser o site correto)

## ✅ Solução: Atualizar Social Application no Django Admin

### 1. Obter Credenciais do Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Vá em: **APIs & Services** > **Credentials**
3. Clique no seu **OAuth 2.0 Client ID**
4. Copie:
   - **Client ID** (exemplo: `123456789-abc.apps.googleusercontent.com`)
   - **Client secret** (exemplo: `GOCSPX-abc123def456`)

### 2. Atualizar Social Application no Django Admin

1. **Acesse o Django Admin:**
   - URL: `http://127.0.0.1:8000/admin/`
   - Faça login com sua conta de administrador

2. **Vá em Social Accounts:**
   - No menu lateral, clique em **Social Accounts** > **Social applications**

3. **Edite a aplicação "Resumo Acadêmico":**
   - Clique na aplicação existente
   - Ou clique em **"Add social application"** se não existir

4. **Preencha os campos:**
   - **Provider:** `Google` (deve estar selecionado)
   - **Name:** `Resumo Acadêmico` (ou outro nome)
   - **Client id:** Cole o **Client ID real** do Google Cloud Console
     - ❌ NÃO use `placeholder`
     - ✅ Use algo como: `123456789-abc.apps.googleusercontent.com`
   - **Secret key:** Cole o **Client Secret real** do Google Cloud Console
     - ❌ NÃO use `placeholder`
     - ✅ Use algo como: `GOCSPX-abc123def456`
   - **Sites:** Selecione o site correto
     - Deve mostrar algo como: `example.com` ou `127.0.0.1:8000`
     - Se não aparecer, você precisa criar/atualizar o site primeiro

5. **Clique em "Save"**

### 3. Verificar Site do Django

Se o site estiver como `example.com`, você precisa atualizar:

1. No Django Admin, vá em **Sites** > **Sites**
2. Clique no site `example.com`
3. Atualize:
   - **Domain name:** `127.0.0.1:8000` (para desenvolvimento)
   - **Display name:** `Resumo Acadêmico`
4. Clique em **Save**

**OU** para produção:
- **Domain name:** `resumoacademico.com.br`
- **Display name:** `Resumo Acadêmico`

## 📋 Checklist de Configuração

- [ ] Credenciais do Google Cloud Console obtidas
- [ ] Client ID real copiado
- [ ] Client Secret real copiado
- [ ] Social Application atualizada no Django Admin
- [ ] Client ID placeholder substituído por valor real
- [ ] Client Secret placeholder substituído por valor real
- [ ] Site correto selecionado na Social Application
- [ ] Site do Django atualizado (se necessário)

## 🧪 Testar Após Configurar

1. **Acesse a página de login:**
   - `http://127.0.0.1:8000/questoes/login/`

2. **Clique em "Continuar com Google"**

3. **Deve redirecionar para o Google:**
   - Você verá a tela de autorização do Google
   - Após autorizar, deve voltar para o Django

4. **Se não funcionar:**
   - Verifique se as credenciais estão corretas
   - Verifique se o site está selecionado
   - Verifique os logs do servidor Django (terminal)
   - Aguarde alguns minutos (propagação do Google)

## ⚠️ Erros Comuns

### Erro: "SocialApp.DoesNotExist"
- **Causa:** Social Application não existe
- **Solução:** Criar uma nova Social Application no Django Admin

### Erro: "redirect_uri_mismatch"
- **Causa:** URL de callback não está autorizada no Google
- **Solução:** Verificar se `http://127.0.0.1:8000/accounts/google/login/callback/` está nas URLs autorizadas

### Erro: "invalid_client"
- **Causa:** Client ID ou Secret incorretos
- **Solução:** Verificar se as credenciais no Django Admin estão corretas

### Erro: "access_denied"
- **Causa:** OAuth Consent Screen não configurado
- **Solução:** Configurar o OAuth Consent Screen no Google Cloud Console

## 🎯 Resumo

1. ✅ Obter credenciais reais do Google Cloud Console
2. ✅ Atualizar Social Application no Django Admin com credenciais reais
3. ✅ Verificar/atualizar site do Django
4. ✅ Testar login com Google

**O problema é que você está usando valores placeholder em vez das credenciais reais do Google!**

