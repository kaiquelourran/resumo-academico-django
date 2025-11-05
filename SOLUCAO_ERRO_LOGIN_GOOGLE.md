# 🔧 Solução para "Falha ao Entrar com Rede Social"

## ⚠️ Erro Identificado

```
Falha ao Entrar com Rede Social
Houve um erro ao tentar entrar com a sua conta de rede social.
```

## 🔍 Possíveis Causas e Soluções

### 1. ⚠️ URL de Callback Não Autorizada no Google

**Sintoma:** Erro "redirect_uri_mismatch"

**Verificar:**
- A URL `http://127.0.0.1:8000/accounts/google/login/callback/` está nas "Authorized redirect URIs" do Google Cloud Console?

**Solução:**
1. Acesse: https://console.cloud.google.com/
2. Vá em: **APIs & Services** > **Credentials**
3. Clique no seu **OAuth 2.0 Client ID**
4. Verifique se estas URLs estão em "Authorized redirect URIs":
   - ✅ `http://localhost:8000/accounts/google/login/callback/`
   - ✅ `http://127.0.0.1:8000/accounts/google/login/callback/`
   - ✅ `https://resumoacademico.com.br/accounts/google/login/callback/`
5. Se não estiverem, **ADICIONE** e clique em **SAVE**

### 2. ⚠️ Client ID ou Secret Incorretos

**Sintoma:** Erro "invalid_client"

**Verificar no Django Admin:**
1. Acesse: `http://127.0.0.1:8000/admin/`
2. Vá em: **Social Accounts** > **Social applications**
3. Clique na aplicação "Resumo Acadêmico"
4. Verifique se:
   - **Client id:** `483177848191-i85ijikssoaftcnam1kjinhkdvi7lf69.apps.googleusercontent.com`
   - **Secret key:** `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`
   - **Sites:** `127.0.0.1:8000` está selecionado

### 3. ⚠️ Site Não Correspondente

**Sintoma:** Erro de site não encontrado

**Verificar:**
- O site no Django Admin deve ser `127.0.0.1:8000`
- O mesmo site deve estar selecionado na Social Application

### 4. ⚠️ OAuth Consent Screen Não Configurado

**Sintoma:** Erro "access_denied"

**Solução:**
1. Acesse: https://console.cloud.google.com/
2. Vá em: **APIs & Services** > **OAuth consent screen**
3. Configure:
   - **User Type:** External (para desenvolvimento)
   - **App name:** Resumo Acadêmico
   - **User support email:** Seu email
   - **Developer contact information:** Seu email
4. Clique em **Save and Continue**

### 5. ⚠️ Propagação do Google Não Completa

**Sintoma:** Erro após configurar tudo corretamente

**Solução:**
- ⏳ Aguarde 5-30 minutos após fazer alterações no Google Cloud Console
- 🔄 Tente novamente após aguardar

## 🔍 Verificar Logs do Servidor Django

**No terminal onde o servidor Django está rodando, procure por:**

```
Error: ...
Exception: ...
redirect_uri_mismatch
invalid_client
access_denied
```

**Se encontrar algum erro, copie a mensagem completa e me envie.**

## 📋 Checklist de Verificação

### Google Cloud Console:
- [ ] Client ID: `483177848191-i85ijikssoaftcnam1kjinhkdvi7lf69.apps.googleusercontent.com`
- [ ] Client Secret: `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`
- [ ] Authorized redirect URIs incluem:
  - [ ] `http://localhost:8000/accounts/google/login/callback/`
  - [ ] `http://127.0.0.1:8000/accounts/google/login/callback/`
  - [ ] `https://resumoacademico.com.br/accounts/google/login/callback/`
- [ ] OAuth Consent Screen configurado

### Django Admin:
- [ ] Social Application existe
- [ ] Client ID correto
- [ ] Client Secret correto
- [ ] Site `127.0.0.1:8000` selecionado

### Django Settings:
- [ ] SITE_ID = 1
- [ ] Site do Django = `127.0.0.1:8000`

## 🧪 Teste Passo a Passo

1. **Verifique os logs do servidor Django** (terminal)
   - Procure por erros quando clicar em "Continuar com Google"

2. **Teste a URL de callback diretamente:**
   - Acesse: `http://127.0.0.1:8000/accounts/google/login/callback/`
   - Deve mostrar erro ou redirecionar (não deve ser 404)

3. **Verifique se o Google redireciona corretamente:**
   - Clique em "Continuar com Google"
   - Deve redirecionar para o Google
   - Após autorizar, deve voltar para o Django

4. **Se não redirecionar para o Google:**
   - Verifique se a Social Application está configurada
   - Verifique se o Client ID está correto

## 🚨 Erro Mais Comum: redirect_uri_mismatch

**Se você ver este erro, significa que:**
- A URL de callback no Google não corresponde à URL que o Django está enviando
- **Solução:** Adicione `http://127.0.0.1:8000/accounts/google/login/callback/` nas URLs autorizadas

## 📝 Próximos Passos

1. ✅ Verifique os logs do servidor Django (terminal)
2. ✅ Verifique se todas as URLs estão no Google Cloud Console
3. ✅ Verifique se as credenciais estão corretas no Django Admin
4. ✅ Aguarde alguns minutos (propagação)
5. ✅ Teste novamente

## 💡 Dica

**Copie qualquer erro que aparecer no terminal do servidor Django** e me envie. Isso ajudará a identificar o problema exato!

