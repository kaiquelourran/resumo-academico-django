# 📦 Instalar Bibliotecas do Google OAuth2

## ✅ Instalação

Execute o seguinte comando para instalar as bibliotecas necessárias:

```bash
pip install google-auth==2.23.4 google-auth-oauthlib==1.1.0 google-auth-httplib2==0.1.1
```

Ou se estiver usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 🔧 Configuração no Google Cloud Console

1. **Acesse o Google Cloud Console:**
   - https://console.cloud.google.com/
   - Vá em **APIs & Services** > **Credentials**

2. **Atualize as "Authorized redirect URIs":**
   - Adicione: `http://127.0.0.1:8000/questoes/google/callback/`
   - Para produção: `https://resumoacademico.com.br/questoes/google/callback/`

3. **Verifique o OAuth 2.0 Client ID:**
   - Certifique-se de que o Client ID e Secret estão corretos no Django Admin
   - Vá em: **Social Accounts** > **Social applications**
   - Verifique se a aplicação "Resumo Acadêmico" está configurada

## ✅ Vantagens desta Solução

1. **Mais Simples:** Usa as bibliotecas oficiais do Google
2. **Mais Direto:** Menos dependências e menos complexidade
3. **Mais Confiável:** Bibliotecas mantidas pelo próprio Google
4. **Login Automático:** Não precisa de páginas intermediárias
5. **Melhor Controle:** Código mais fácil de entender e debugar

## 🔄 Como Funciona

1. Usuário clica em "Continuar com Google"
2. Redireciona para `/questoes/google/login/`
3. A view redireciona para o Google OAuth
4. Google autoriza e redireciona para `/questoes/google/callback/`
5. A view processa o token e faz login automático
6. Redireciona para `/questoes/index/`

## 📝 Notas

- As credenciais do Google ainda são obtidas do Django Admin (SocialApp)
- Não precisa configurar nada adicional no `settings.py`
- O código é mais simples e fácil de manter

