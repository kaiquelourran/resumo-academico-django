# 🔧 Como Corrigir o Erro "redirect_uri_mismatch"

## ⚠️ Erro

```
Erro 400: redirect_uri_mismatch
Não é possível fazer login porque Resumo Acadêmico enviou uma solicitação inválida.
```

## 🔍 Causa

A URI de callback que o código está enviando **não corresponde exatamente** a uma das URIs autorizadas no Google Cloud Console.

## ✅ Solução

### 1. Verificar a URI que está sendo enviada

Execute o servidor Django e tente fazer login. Os logs mostrarão a URI que está sendo construída:

```
INFO: Callback URL construída: http://127.0.0.1:8000/questoes/google/callback/
INFO: HTTP_HOST: 127.0.0.1:8000
INFO: Request scheme: http
```

### 2. Verificar as URIs no Google Cloud Console

Acesse: https://console.cloud.google.com/ > APIs & Services > Credentials

**As URIs devem ser EXATAMENTE iguais, incluindo:**
- ✅ Protocolo (`http://` ou `https://`)
- ✅ Domínio (`127.0.0.1` ou `localhost`)
- ✅ Porta (`:8000`)
- ✅ Caminho completo (`/questoes/google/callback/`)
- ✅ Barra final (`/`)

### 3. URIs que DEVEM estar configuradas

**Para desenvolvimento local:**
```
http://127.0.0.1:8000/questoes/google/callback/
http://localhost:8000/questoes/google/callback/
```

**Para produção:**
```
https://resumoacademico.com.br/questoes/google/callback/
```

### 4. Verificar se a URI está correta no código

O código usa `request.build_absolute_uri('/questoes/google/callback/')` que constrói a URI baseada em:
- `request.scheme` (http ou https)
- `request.META['HTTP_HOST']` (host:port)

**Se estiver usando `http://127.0.0.1:8000`:**
- A URI será: `http://127.0.0.1:8000/questoes/google/callback/`
- Esta URI **DEVE** estar no Google Cloud Console

**Se estiver usando `http://localhost:8000`:**
- A URI será: `http://localhost:8000/questoes/google/callback/`
- Esta URI **DEVE** estar no Google Cloud Console

## 🎯 Solução Rápida

### Opção 1: Adicionar todas as variações (Recomendado)

Adicione TODAS estas URIs no Google Cloud Console:

```
http://127.0.0.1:8000/questoes/google/callback/
http://localhost:8000/questoes/google/callback/
https://resumoacademico.com.br/questoes/google/callback/
```

### Opção 2: Forçar uma URI específica no código

Se quiser usar sempre a mesma URI, modifique `questoes/google_auth.py`:

```python
# Em vez de:
callback_url = request.build_absolute_uri('/questoes/google/callback/')

# Use:
callback_url = 'http://127.0.0.1:8000/questoes/google/callback/'  # Para desenvolvimento
# ou
callback_url = 'https://resumoacademico.com.br/questoes/google/callback/'  # Para produção
```

## 📝 Checklist

- [ ] Verificar os logs do Django para ver qual URI está sendo construída
- [ ] Comparar com as URIs no Google Cloud Console
- [ ] Adicionar a URI exata que está faltando
- [ ] Clicar em "SAVE" no Google Cloud Console
- [ ] Testar novamente o login

## ⚠️ Importante

- As URIs são **case-sensitive** (maiúsculas/minúsculas importam)
- As URIs devem ter a **barra final** (`/`)
- O protocolo (`http://` vs `https://`) deve corresponder
- O domínio (`127.0.0.1` vs `localhost`) deve corresponder
- A porta (`:8000`) deve corresponder

## 🔍 Debug

Para ver qual URI está sendo enviada, verifique os logs do Django após tentar fazer login. O código agora loga a URI construída.

