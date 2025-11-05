# Configuração do Google OAuth

## Passos para configurar o login com Google

### 1. Criar um projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Crie um novo projeto ou selecione um existente
3. Vá em **APIs & Services** > **Credentials**
4. Clique em **Create Credentials** > **OAuth client ID**

### 2. Configurar o OAuth Consent Screen

1. Vá em **APIs & Services** > **OAuth consent screen**
2. Escolha **External** (para desenvolvimento)
3. Preencha:
   - **App name**: Resumo Acadêmico
   - **User support email**: Seu email
   - **Developer contact information**: Seu email
4. Clique em **Save and Continue**

### 3. Criar as credenciais OAuth

1. Vá em **APIs & Services** > **Credentials**
2. Clique em **Create Credentials** > **OAuth client ID**
3. Escolha **Web application**
4. Configure:
   - **Name**: Resumo Acadêmico Web Client
   - **Authorized JavaScript origins**: 
     - `http://localhost:8000` (desenvolvimento)
     - `http://localhost` (desenvolvimento alternativo)
     - `https://resumoacademico.com.br` (produção)
   - **Authorized redirect URIs** (IMPORTANTE: Use estas URLs do Django, não URLs PHP):
     - `http://localhost:8000/accounts/google/login/callback/` (desenvolvimento)
     - `https://resumoacademico.com.br/accounts/google/login/callback/` (produção)
     - **⚠️ NÃO use URLs como `/questoes/processar_google_login.php` - essas são do sistema antigo PHP!**
5. Clique em **Create**
6. Copie o **Client ID** e o **Client secret**

### 4. Configurar variáveis de ambiente

Adicione ao seu arquivo `.env`:

```env
GOOGLE_CLIENT_ID=seu_client_id_aqui.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=seu_client_secret_aqui
```

### 5. Configurar Social Application no Django Admin

**NOTA**: Uma Social Application já foi criada automaticamente com valores placeholder. Você precisa atualizar com as credenciais reais do Google.

1. Acesse o Django Admin: `http://localhost:8000/admin/`
2. Vá em **Social Accounts** > **Social applications**
3. Clique na aplicação "Resumo Acadêmico" existente (ou crie uma nova se não existir)
4. Atualize os campos:
   - **Provider**: Google (deve estar selecionado)
   - **Name**: Resumo Acadêmico
   - **Client id**: Cole o Client ID real do Google Cloud Console (substitua "placeholder")
   - **Secret key**: Cole o Client Secret real do Google Cloud Console (substitua "placeholder")
   - **Sites**: Selecione o site (exemplo.com) - deve estar marcado
5. Clique em **Save**

### 6. Verificar configuração

1. Acesse: `http://localhost:8000/questoes/login/`
2. Clique no botão **Continuar com Google**
3. Você será redirecionado para o Google para autorizar
4. Após autorizar, será redirecionado de volta para a aplicação

## Notas Importantes

- **Desenvolvimento**: Use `http://localhost:8000` nas URLs autorizadas
- **Produção**: Substitua `localhost:8000` pelo seu domínio real
- **HTTPS**: Em produção, use sempre HTTPS
- **Variáveis de ambiente**: Nunca commite o `.env` com credenciais reais no Git

## Troubleshooting

### Erro: "redirect_uri_mismatch"
- Verifique se a URL de callback está exatamente igual no Google Cloud Console
- Certifique-se de incluir a barra final (`/`) na URL

### Erro: "invalid_client"
- Verifique se o Client ID e Secret estão corretos no `.env`
- Verifique se criou a Social Application no Django Admin

### Erro: "access_denied"
- Verifique se o OAuth Consent Screen está configurado corretamente
- Em desenvolvimento, pode ser necessário adicionar usuários de teste

