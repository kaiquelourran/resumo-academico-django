# 🔍 Como Debugar o Login com Google

## ⚠️ Problema

Após clicar em "Continuar com Google", você vê um aviso do console do navegador e é redirecionado de volta para a página de login.

## 🔍 Passos para Debugar

### 1. Verificar os Logs do Django

Execute o servidor Django e observe os logs no terminal:

```bash
python manage.py runserver
```

Quando você tentar fazer login com Google, você verá logs detalhados como:

```
INFO: === INÍCIO DO CALLBACK DO GOOGLE ===
INFO: Request GET params: {'code': '...', 'scope': '...'}
INFO: Request META HTTP_HOST: 127.0.0.1:8000
INFO: Código de autorização recebido: 4/0Ab32j91...
INFO: Client ID obtido: 483177848191-i85ijik...
INFO: Callback URL usada no callback: http://127.0.0.1:8000/questoes/google/callback/
INFO: Enviando requisição para obter token...
INFO: Status da resposta do token: 200
INFO: Token recebido com sucesso
INFO: Verificando e decodificando ID token...
INFO: ID token verificado com sucesso
INFO: Email extraído: seuemail@gmail.com
INFO: Nome: Seu Nome
INFO: Buscando ou criando usuário...
INFO: Usuário criado: seuemail@gmail.com
INFO: Fazendo login do usuário...
INFO: Login realizado com sucesso para: seuemail@gmail.com
INFO: === FIM DO CALLBACK DO GOOGLE - SUCESSO ===
```

### 2. Verificar Erros Específicos

Se houver um erro, você verá algo como:

```
ERROR: === ERRO NO CALLBACK DO GOOGLE ===
ERROR: Erro ao processar callback do Google: [mensagem do erro]
ERROR: Tipo do erro: [tipo do erro]
ERROR: Traceback completo:
[stack trace completo]
```

### 3. Possíveis Erros e Soluções

#### Erro: "redirect_uri_mismatch"
**Causa:** A URI de callback não corresponde exatamente às URIs no Google Cloud Console.

**Solução:**
1. Verifique os logs para ver qual URI está sendo enviada
2. Compare com as URIs no Google Cloud Console
3. Adicione a URI exata que está faltando

#### Erro: "invalid_client"
**Causa:** Client ID ou Secret incorretos.

**Solução:**
1. Verifique no Django Admin: Social Accounts > Social applications
2. Confirme que o Client ID e Secret estão corretos
3. Verifique se o Client ID corresponde ao do Google Cloud Console

#### Erro: "Token ID não recebido"
**Causa:** O Google não retornou o ID token na resposta.

**Solução:**
1. Verifique os logs para ver a resposta completa do Google
2. Verifique se o Client ID está correto
3. Verifique se o redirect_uri está correto

#### Erro: "Email não encontrado no token"
**Causa:** O token do Google não contém o email do usuário.

**Solução:**
1. Verifique se o scope inclui 'email'
2. Verifique se o usuário autorizou o acesso ao email

### 4. Verificar a URL de Callback

Quando você clica em "Continuar com Google", verifique os logs para ver:

```
INFO: Callback URL construída: http://127.0.0.1:8000/questoes/google/callback/
INFO: HTTP_HOST: 127.0.0.1:8000
INFO: Request scheme: http
```

**Esta URI deve corresponder EXATAMENTE a uma das URIs no Google Cloud Console.**

### 5. Testar o Fluxo Completo

1. **Acesse a página de login:**
   ```
   http://127.0.0.1:8000/questoes/login/
   ```

2. **Clique em "Continuar com Google"**

3. **Observe os logs no terminal:**
   - Deve aparecer "Callback URL construída"
   - Deve redirecionar para o Google
   - Após autorizar, deve voltar para o callback
   - Deve aparecer "=== INÍCIO DO CALLBACK DO GOOGLE ==="

4. **Se houver erro, os logs mostrarão exatamente onde está o problema**

## 📋 Checklist de Verificação

- [ ] Client ID e Secret estão corretos no Django Admin
- [ ] A URI de callback está no Google Cloud Console
- [ ] A URI no código corresponde exatamente à do Google Cloud Console
- [ ] Os logs mostram o fluxo completo
- [ ] Não há erros nos logs após o callback

## 🎯 Próximos Passos

1. Execute o servidor Django
2. Tente fazer login com Google
3. Copie os logs completos do terminal
4. Envie os logs para análise

Os logs agora são muito detalhados e mostrarão exatamente onde está o problema!

