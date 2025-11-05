"""
Módulo simplificado para login com Google usando a biblioteca oficial do Google OAuth2.
Mais simples e direto que django-allauth.
"""
from django.shortcuts import redirect
from django.contrib.auth import login, get_user_model
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests
import json
import logging

logger = logging.getLogger(__name__)
# Configurar logger para garantir que os logs apareçam
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

User = get_user_model()

# Configurações do Google OAuth (deve ser configurado no Django Admin ou settings)
GOOGLE_CLIENT_ID = None  # Será obtido do SocialApp ou settings


def get_google_client_id():
    """Obtém o Client ID do Google do Django Admin ou settings"""
    try:
        from allauth.socialaccount.models import SocialApp
        app = SocialApp.objects.get(provider='google')
        return app.client_id
    except:
        # Se não encontrar no allauth, tenta pegar do settings
        return getattr(settings, 'GOOGLE_CLIENT_ID', None)


def google_login_redirect(request):
    """
    Redireciona para a página de autorização do Google.
    """
    client_id = get_google_client_id()
    if not client_id:
        from django.contrib import messages
        messages.error(request, 'Login com Google não está configurado.')
        return redirect('questoes:login')
    
    # URL de callback - deve corresponder EXATAMENTE às URIs configuradas no Google Cloud Console
    # Usa request.build_absolute_uri() para garantir que seja construída corretamente
    callback_url = request.build_absolute_uri('/questoes/google/callback/')
    
    # Remove a barra final se não tiver (alguns casos)
    # Mas normalmente o Google espera COM a barra final
    if not callback_url.endswith('/'):
        callback_url += '/'
    
    # Log para debug - usar print também para garantir que apareça
    print('=== INÍCIO DO LOGIN COM GOOGLE ===')
    print(f'Callback URL construída: {callback_url}')
    print(f'HTTP_HOST: {request.META.get("HTTP_HOST", "N/A")}')
    print(f'Request scheme: {request.scheme}')
    print(f'Request path: {request.path}')
    print(f'Request get_host(): {request.get_host()}')
    
    logger.info('=== INÍCIO DO LOGIN COM GOOGLE ===')
    logger.info(f'Callback URL construída: {callback_url}')
    logger.info(f'HTTP_HOST: {request.META.get("HTTP_HOST", "N/A")}')
    logger.info(f'Request scheme: {request.scheme}')
    logger.info(f'Request path: {request.path}')
    logger.info(f'Request get_host(): {request.get_host()}')
    
    # Verifica se a URI está correta
    # Deve ser uma das seguintes:
    # - http://127.0.0.1:8000/questoes/google/callback/
    # - http://localhost:8000/questoes/google/callback/
    # - https://resumoacademico.com.br/questoes/google/callback/
    expected_uris = [
        'http://127.0.0.1:8000/questoes/google/callback/',
        'http://localhost:8000/questoes/google/callback/',
        'https://resumoacademico.com.br/questoes/google/callback/',
    ]
    
    if callback_url not in expected_uris:
        logger.warning(f'⚠️ URI construída não está na lista esperada: {callback_url}')
        logger.warning(f'URIs esperadas: {expected_uris}')
        logger.warning(f'⚠️ Certifique-se de que esta URI está no Google Cloud Console!')
    
    # Parâmetros OAuth2 do Google
    auth_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'client_id': client_id,
        'redirect_uri': callback_url,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'online',
        'prompt': 'select_account',
    }
    
    print(f'Client ID usado: {client_id[:20]}...')
    print(f'Redirect URI que será enviado ao Google: {callback_url}')
    print('⚠️ VERIFIQUE SE ESTA URI ESTÁ NO GOOGLE CLOUD CONSOLE!')
    
    logger.info(f'Client ID usado: {client_id[:20]}...')
    logger.info(f'Redirect URI que será enviado ao Google: {callback_url}')
    
    # Salva o callback_url na sessão para usar no callback
    request.session['google_callback_url'] = callback_url
    
    # Constrói a URL completa
    from urllib.parse import urlencode
    auth_url_with_params = f"{auth_url}?{urlencode(params)}"
    
    print(f'URL de autorização completa: {auth_url_with_params[:100]}...')
    print('=== FIM DO LOGIN COM GOOGLE - REDIRECIONANDO ===')
    
    logger.info(f'URL de autorização completa: {auth_url_with_params[:100]}...')
    logger.info('=== FIM DO LOGIN COM GOOGLE - REDIRECIONANDO ===')
    
    return redirect(auth_url_with_params)


def google_callback(request):
    """
    Processa o callback do Google OAuth2 e faz login automático.
    """
    from django.contrib import messages
    
    logger.info('=== INÍCIO DO CALLBACK DO GOOGLE ===')
    logger.info(f'Request GET params: {request.GET}')
    logger.info(f'Request META HTTP_HOST: {request.META.get("HTTP_HOST", "N/A")}')
    
    # Verifica se tem código de autorização
    code = request.GET.get('code')
    error_param = request.GET.get('error')
    
    if error_param:
        logger.error(f'Erro recebido do Google: {error_param}')
        error_description = request.GET.get('error_description', 'Erro desconhecido')
        messages.error(request, f'Erro ao fazer login com Google: {error_description}')
        return redirect('questoes:login')
    
    if not code:
        logger.error('Código de autorização não recebido do Google')
        messages.error(request, 'Erro ao fazer login com Google: código de autorização não recebido.')
        return redirect('questoes:login')
    
    logger.info(f'Código de autorização recebido: {code[:20]}...')
    
    try:
        # Obtém o Client ID e Secret
        from allauth.socialaccount.models import SocialApp
        app = SocialApp.objects.get(provider='google')
        client_id = app.client_id
        client_secret = app.secret
        
        logger.info(f'Client ID obtido: {client_id[:20]}...')
        
        # Obtém a URL de callback da sessão ou constrói novamente
        # Deve corresponder EXATAMENTE à URI configurada no Google Cloud Console
        callback_url = request.session.get('google_callback_url')
        if not callback_url:
            callback_url = request.build_absolute_uri('/questoes/google/callback/')
            if not callback_url.endswith('/'):
                callback_url += '/'
        
        logger.info(f'Callback URL usada no callback: {callback_url}')
        
        # Troca o código de autorização por um access token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': callback_url,
            'grant_type': 'authorization_code',
        }
        
        logger.info(f'Enviando requisição para obter token...')
        logger.info(f'Token URL: {token_url}')
        logger.info(f'Redirect URI usado: {callback_url}')
        
        token_response = requests.post(token_url, data=token_data)
        
        logger.info(f'Status da resposta do token: {token_response.status_code}')
        
        if token_response.status_code != 200:
            logger.error(f'Erro ao obter token: {token_response.status_code}')
            logger.error(f'Resposta: {token_response.text}')
            raise ValueError(f'Erro ao obter token do Google: {token_response.status_code} - {token_response.text}')
        
        token_info = token_response.json()
        logger.info('Token recebido com sucesso')
        
        id_token_str = token_info.get('id_token')
        if not id_token_str:
            logger.error('Token ID não encontrado na resposta')
            raise ValueError('Token ID não recebido do Google')
        
        logger.info('Verificando e decodificando ID token...')
        
        # Verifica e decodifica o ID token
        try:
            idinfo = id_token.verify_oauth2_token(
                id_token_str, 
                google_requests.Request(), 
                client_id
            )
            logger.info('ID token verificado com sucesso')
        except Exception as verify_error:
            logger.error(f'Erro ao verificar ID token: {verify_error}')
            raise ValueError(f'Erro ao verificar token do Google: {str(verify_error)}')
        
        # Extrai informações do usuário
        email = idinfo.get('email')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        picture = idinfo.get('picture', '')
        
        logger.info(f'Email extraído: {email}')
        logger.info(f'Nome: {first_name} {last_name}')
        
        if not email:
            logger.error('Email não encontrado no token')
            raise ValueError('Email não encontrado no token do Google')
        
        # Busca ou cria o usuário
        # POLÍTICA: Cada email só pode ter UM usuário no sistema
        # Se já existir (cadastro manual ou Google anterior), faz login no existente
        logger.info('Buscando ou criando usuário...')
        
        # Busca usuários existentes com este email
        # Ordena por data de criação (mais antigo primeiro) para usar o original
        existing_users = User.objects.filter(email=email).order_by('date_joined')
        
        if existing_users.exists():
            # Email já cadastrado - usa o usuário existente (mais antigo se houver múltiplos)
            # Prioriza usuário ativo
            user = existing_users.filter(is_active=True).first()
            if not user:
                user = existing_users.first()  # Usa o mais antigo
            
            created = False
            logger.info(f'✅ Email já cadastrado. Usando usuário existente: {user.email} (ID: {user.id}, Criado: {user.date_joined})')
            
            # Se há múltiplos usuários, loga um aviso (caso de migração)
            if existing_users.count() > 1:
                logger.warning(f'⚠️ AVISO: Encontrados {existing_users.count()} usuários com o email {email}.')
                logger.warning(f'⚠️ Usando o usuário mais antigo (ID: {user.id}, Criado: {user.date_joined})')
                logger.warning(f'⚠️ Outros usuários: {list(existing_users.exclude(id=user.id).values_list("id", "username", "date_joined"))}')
                print(f'⚠️ AVISO: Múltiplos usuários encontrados para {email}. Usando o mais antigo (ID: {user.id})')
        else:
            # Email NÃO cadastrado - cria novo usuário
            # Verifica se o username já existe e ajusta se necessário
            base_username = email.split('@')[0][:150]
            username = base_username
            counter = 1
            
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"[:150]
                counter += 1
            
            user = User.objects.create(
                email=email,
                username=username,
                first_name=first_name[:30],
                last_name=last_name[:30],
                is_active=True,
            )
            created = True
            logger.info(f'✅ Novo usuário criado: {user.email} (ID: {user.id}, Username: {user.username})')
            print(f'✅ Novo usuário criado: {user.email} (ID: {user.id})')
        
        # Atualiza as informações do usuário
        if not created:
            updated = False
            if first_name and not user.first_name:
                user.first_name = first_name[:30]
                updated = True
            if last_name and not user.last_name:
                user.last_name = last_name[:30]
                updated = True
            if not user.is_active:
                user.is_active = True
                updated = True
            
            if updated:
                user.save()
                logger.info(f'Informações do usuário atualizadas: {user.email}')
        
        # Faz login automático
        logger.info('Fazendo login do usuário...')
        print(f'Fazendo login do usuário ID: {user.id}, Email: {user.email}')
        print(f'Usuário antes do login - is_authenticated: {request.user.is_authenticated}')
        
        # Garantir que o usuário está ativo
        if not user.is_active:
            logger.warning(f'Usuário {user.email} está inativo. Ativando...')
            user.is_active = True
            user.save()
        
        # Fazer login (não precisa salvar sessão antes, o Django faz isso automaticamente)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Verificar se o login foi bem-sucedido
        if not request.user.is_authenticated:
            logger.error(f'❌ ERRO: Login falhou! Usuário NÃO está autenticado após login()')
            print(f'❌ ERRO: Login falhou! Usuário NÃO está autenticado após login()')
            messages.error(request, 'Erro ao fazer login. Por favor, tente novamente.')
            return redirect('questoes:login')
        
        logger.info(f'✅ Login realizado com sucesso! Usuário autenticado: {request.user.email}')
        print(f'✅ Login realizado com sucesso! Usuário autenticado: {request.user.email}')
        print(f'Session key: {request.session.session_key}')
        print(f'User ID: {request.user.id}')
        
        if created:
            messages.success(request, f'Bem-vindo(a), {user.first_name or user.username}! Conta criada com sucesso.')
        else:
            messages.success(request, f'Bem-vindo(a), {user.first_name or user.username}!')
        
        logger.info('=== FIM DO CALLBACK DO GOOGLE - SUCESSO ===')
        logger.info(f'Redirecionando para: /questoes/index/')
        print(f'✅ Redirecionando para: /questoes/index/')
        print(f'✅ Usuário final autenticado: {request.user.is_authenticated}, Email: {request.user.email}')
        
        # Redirecionar para a página inicial
        return redirect('/questoes/index/')
        
    except Exception as e:
        logger.error('=== ERRO NO CALLBACK DO GOOGLE ===')
        logger.error(f'Erro ao processar callback do Google: {e}', exc_info=True)
        logger.error(f'Tipo do erro: {type(e).__name__}')
        import traceback
        logger.error(f'Traceback completo:\n{traceback.format_exc()}')
        
        messages.error(request, f'Erro ao fazer login com Google: {str(e)}. Por favor, tente novamente.')
        return redirect('questoes:login')

