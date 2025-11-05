# 🔒 Migração Segura do Google OAuth - PHP para Django

## ✅ Resposta Rápida

**NÃO, seu site PHP NÃO vai cair!** Mudar as URLs de redirecionamento no Google Cloud Console é apenas uma configuração do Google e não afeta seu site atual.

## 📋 Como Funciona

### O que são as "Authorized redirect URIs"?

As URLs de redirecionamento no Google Cloud Console são apenas **destinos** para onde o Google redireciona o usuário **após** a autenticação bem-sucedida.

- **NÃO** afetam o funcionamento do seu site PHP atual
- **NÃO** mudam nenhum código do seu servidor
- **NÃO** alteram banco de dados ou arquivos
- São apenas **configurações de segurança** do Google

### Fluxo de Autenticação

```
1. Usuário clica em "Login com Google" no seu site
2. Usuário é redirecionado para o Google (autenticação)
3. Google verifica qual URL está autorizada
4. Google redireciona de volta para a URL autorizada (callback)
5. Seu servidor processa o login
```

## 🛡️ Opções de Migração Segura

### Opção 1: Migração Gradual (Recomendado)

Manter ambas as URLs temporariamente durante a migração:

**Authorized redirect URIs:**
```
http://localhost:8000/accounts/google/login/callback/  (Django - novo)
https://resumoacademico.com.br/questoes/processar_google_login.php  (PHP - antigo, mantém funcionando)
```

**Vantagens:**
- ✅ Site PHP continua funcionando normalmente
- ✅ Pode testar o Django localmente sem afetar produção
- ✅ Migração gradual sem risco

**Quando remover a URL PHP:**
- Após confirmar que o Django está funcionando 100% em produção
- Após migrar todos os usuários para o novo sistema

### Opção 2: Migração Completa (Futuro)

Quando estiver pronto para migrar completamente:

1. **Teste o Django localmente** primeiro
2. **Configure o Django na Hostinger** (pode rodar junto com PHP)
3. **Teste em produção** com o Django
4. **Depois** remova a URL PHP do Google Cloud Console

## 📝 Passos Seguros para Adicionar URLs Django

### Passo 1: Adicionar (NÃO substituir)

No Google Cloud Console, **ADICIONE** as novas URLs Django **sem remover** as URLs PHP:

**Authorized redirect URIs (mantenha todas):**
```
http://localhost:8000/accounts/google/login/callback/  ← ADICIONE ESTA
https://resumoacademico.com.br/accounts/google/login/callback/  ← ADICIONE ESTA
http://localhost:8000/RESUMO%20ACAD%C3%8AMICO/questoes/processar_google_login.php  ← MANTENHA (se ainda usar)
https://resumoacademico.com.br/questoes/processar_google_login.php  ← MANTENHA (se ainda usar)
```

### Passo 2: Testar Localmente

1. Configure o Django localmente
2. Teste o login com Google usando: `http://localhost:8000/accounts/google/login/callback/`
3. Se funcionar, o site PHP não foi afetado

### Passo 3: Quando Migrar em Produção

1. Configure o Django na Hostinger (pode coexistir com PHP)
2. Teste o login com Google em produção
3. **Só então** remova as URLs PHP antigas

## ⚠️ Importante

### O que NÃO afeta o site PHP:

- ✅ Adicionar URLs Django no Google Cloud Console
- ✅ Configurar o Django localmente
- ✅ Testar o Django em localhost
- ✅ Mudar URLs de redirecionamento no Google

### O que PODE afetar (se você fizer):

- ❌ Remover/substituir arquivos PHP no servidor
- ❌ Mudar configurações do servidor web (Apache/Nginx)
- ❌ Remover URLs PHP do Google sem ter Django funcionando

## 🎯 Recomendação

**Para agora (desenvolvimento):**

1. ✅ Adicione as URLs Django no Google Cloud Console
2. ✅ Mantenha as URLs PHP também (não remova ainda)
3. ✅ Teste o Django localmente
4. ✅ Seu site PHP continua funcionando normalmente

**Para depois (produção):**

1. Configure o Django na Hostinger
2. Teste tudo em produção
3. Só então remova as URLs PHP antigas

## 📞 Resumo

- **Mudar URLs no Google Cloud Console = SEGURO** ✅
- **Não afeta seu site PHP atual** ✅
- **Pode manter ambas as URLs durante a migração** ✅
- **Remover URLs PHP só depois que Django estiver funcionando** ✅

