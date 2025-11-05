# 🔧 Solução para Erro "redirect_uri_mismatch"

## ⚠️ Erro

```
Erro 400: redirect_uri_mismatch
Acesso bloqueado: a solicitação do app Resumo Acadêmico é inválida
```

## 🔍 Causa

A URI de callback que o código está enviando **não corresponde exatamente** a uma das URIs autorizadas no Google Cloud Console.

## ✅ Solução Passo a Passo

### 1. Verificar a URI que está sendo enviada

Execute o servidor Django e tente fazer login. Os logs mostrarão:

```
INFO: === INÍCIO DO LOGIN COM GOOGLE ===
INFO: Callback URL construída: http://127.0.0.1:8000/questoes/google/callback/
INFO: HTTP_HOST: 127.0.0.1:8000
INFO: Request scheme: http
INFO: Redirect URI que será enviado ao Google: http://127.0.0.1:8000/questoes/google/callback/
```

**Copie a URI exata que aparece nos logs!**

### 2. Verificar as URIs no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Vá em: **APIs & Services** > **Credentials**
3. Clique no seu **OAuth 2.0 Client ID**
4. Role até **"Authorized redirect URIs"**

### 3. Comparar e Adicionar a URI Exata

**A URI nos logs DEVE corresponder EXATAMENTE a uma das URIs no Google Cloud Console.**

**Exemplos de URIs que devem estar configuradas:**

```
http://127.0.0.1:8000/questoes/google/callback/
http://localhost:8000/questoes/google/callback/
https://resumoacademico.com.br/questoes/google/callback/
```

**IMPORTANTE:**
- ✅ Protocolo (`http://` ou `https://`)
- ✅ Domínio (`127.0.0.1` ou `localhost`)
- ✅ Porta (`:8000`)
- ✅ Caminho completo (`/questoes/google/callback/`)
- ✅ Barra final (`/`)

**TUDO deve corresponder EXATAMENTE!**

### 4. Adicionar a URI que Está Faltando

1. Nos logs, copie a URI exata que aparece em "Redirect URI que será enviado ao Google"
2. No Google Cloud Console, clique em **"+ Adicionar URI"**
3. Cole a URI exata dos logs
4. Clique em **"SAVE"**

### 5. Testar Novamente

1. Aguarde alguns segundos (o Google pode levar alguns segundos para atualizar)
2. Tente fazer login novamente
3. Se ainda der erro, verifique os logs novamente e compare com as URIs no Google Cloud Console

## 🎯 Exemplo Prático

**Se os logs mostrarem:**
```
INFO: Redirect URI que será enviado ao Google: http://127.0.0.1:8000/questoes/google/callback/
```

**Então no Google Cloud Console você DEVE ter:**
```
http://127.0.0.1:8000/questoes/google/callback/
```

**Se os logs mostrarem:**
```
INFO: Redirect URI que será enviado ao Google: http://localhost:8000/questoes/google/callback/
```

**Então no Google Cloud Console você DEVE ter:**
```
http://localhost:8000/questoes/google/callback/
```

## 📋 Checklist

- [ ] Execute o servidor Django
- [ ] Tente fazer login com Google
- [ ] Copie a URI exata dos logs (linha "Redirect URI que será enviado ao Google")
- [ ] Abra o Google Cloud Console
- [ ] Compare a URI dos logs com as URIs no Google Cloud Console
- [ ] Adicione a URI exata que está faltando
- [ ] Clique em "SAVE"
- [ ] Aguarde alguns segundos
- [ ] Tente fazer login novamente

## ⚠️ Erros Comuns

1. **URI com barra final diferente:**
   - ❌ `http://127.0.0.1:8000/questoes/google/callback` (sem barra final)
   - ✅ `http://127.0.0.1:8000/questoes/google/callback/` (com barra final)

2. **Protocolo diferente:**
   - ❌ `https://127.0.0.1:8000/questoes/google/callback/` (https no localhost)
   - ✅ `http://127.0.0.1:8000/questoes/google/callback/` (http no localhost)

3. **Domínio diferente:**
   - ❌ `http://127.0.0.1:8000/questoes/google/callback/` (nos logs)
   - ✅ `http://localhost:8000/questoes/google/callback/` (no Google Cloud)
   - **Solução:** Adicione AMBAS as URIs no Google Cloud Console

## 🎯 Solução Rápida

**Adicione TODAS estas URIs no Google Cloud Console:**

```
http://127.0.0.1:8000/questoes/google/callback/
http://localhost:8000/questoes/google/callback/
https://resumoacademico.com.br/questoes/google/callback/
```

**Isso cobre todas as possibilidades!**

