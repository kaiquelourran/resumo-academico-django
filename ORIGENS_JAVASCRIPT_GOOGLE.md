# 🌐 Origens JavaScript Autorizadas para Google Cloud Console

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

## 📝 Lista Completa para Copiar e Colar

**Cole estas URLs no campo "Authorized JavaScript origins" do Google Cloud Console:**

```
http://localhost:8000
http://localhost
https://resumoacademico.com.br
```

## ⚠️ Importante

1. **Uma URL por linha** no Google Cloud Console
2. **NÃO inclua barra final** (`/`) nas origens JavaScript
3. **Use `http://` para localhost** (desenvolvimento)
4. **Use `https://` para produção** (Hostinger)
5. **NÃO inclua caminhos** (apenas domínio e porta)

## 📍 Onde Colocar

1. Acesse: https://console.cloud.google.com/
2. Vá em: **APIs & Services** > **Credentials**
3. Clique no seu **OAuth 2.0 Client ID**
4. Role até a seção **"Authorized JavaScript origins"**
5. Clique em **"ADD URI"** para cada URL
6. Cole as URLs uma por uma
7. Clique em **"SAVE"** no final

## ✅ Verificação Final

Após salvar, você deve ter **3 URLs** no total:
- `http://localhost:8000` (desenvolvimento)
- `http://localhost` (desenvolvimento alternativo)
- `https://resumoacademico.com.br` (produção)

## 🔍 Diferença entre "Authorized JavaScript origins" e "Authorized redirect URIs"

### "Authorized JavaScript origins" (Origens JavaScript):
- ✅ Apenas domínio e porta
- ✅ Sem barra final (`/`)
- ✅ Sem caminhos (`/accounts/...`)
- Exemplo: `http://localhost:8000`

### "Authorized redirect URIs" (URIs de Redirecionamento):
- ✅ Domínio completo + caminho
- ✅ Com barra final (`/`)
- ✅ Inclui o caminho completo
- Exemplo: `http://localhost:8000/accounts/google/login/callback/`

## 📋 Resumo Completo

**Authorized JavaScript origins (3 URLs):**
```
http://localhost:8000
http://localhost
https://resumoacademico.com.br
```

**Authorized redirect URIs (4 URLs):**
```
http://localhost:8000/accounts/google/login/callback/
https://resumoacademico.com.br/accounts/google/login/callback/
http://localhost:8000/RESUMO%20ACAD%C3%8AMICO/questoes/processar_google_login.php
https://resumoacademico.com.br/questoes/processar_google_login.php
```

