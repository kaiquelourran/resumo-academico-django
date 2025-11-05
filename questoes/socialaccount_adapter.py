"""
Adapter customizado para django-allauth que pula a página de confirmação
ao fazer login com Google e faz login automático.
"""
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth import login
from django.contrib.messages import success
from django.shortcuts import redirect
from django.urls import reverse


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Adapter que pula a página de confirmação e faz login automático."""
    
    def is_open_for_signup(self, request, sociallogin):
        """
        Permite cadastro automático via Google.
        """
        return True
    
    def pre_social_login(self, request, sociallogin):
        """
        Intercepta antes do login social e verifica se o usuário já existe.
        Se existir, conecta e faz login automático, pulando a página de confirmação.
        """
        # Se o usuário já está autenticado, não faz nada
        if request.user.is_authenticated:
            return
        
        # Se o social account já existe, faz login automático (já tratado pelo allauth)
        if sociallogin.is_existing:
            return
        
        # Se tem um email associado, verifica se já existe um usuário
        if sociallogin.email_addresses:
            email = sociallogin.email_addresses[0].email
            try:
                # Verifica se já existe um usuário com esse email
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(email=email)
                # Se existe, conecta a conta social e faz login automático
                sociallogin.connect(request, user)
                login(request, user)
                success(request, f'Bem-vindo(a), {user.first_name or user.username}!')
            except User.DoesNotExist:
                # Se não existe, vai criar automaticamente (SOCIALACCOUNT_AUTO_SIGNUP = True)
                # Mas ainda assim vamos fazer login automático após salvar
                pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Salva o usuário e faz login automático, pulando a página de confirmação.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Faz login automático após salvar o usuário (novo cadastro)
        if not request.user.is_authenticated:
            login(request, user)
            success(request, f'Bem-vindo(a), {user.first_name or user.username}!')
        
        return user
    
    def populate_user(self, request, sociallogin, data):
        """
        Personaliza a criação do usuário a partir dos dados do Google.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Usa o nome do Google se disponível
        if data.get('given_name'):
            user.first_name = data.get('given_name', '')[:30]
        if data.get('family_name'):
            user.last_name = data.get('family_name', '')[:30]
        
        # Se não tem nome, usa o email como fallback
        if not user.first_name and data.get('email'):
            user.first_name = data.get('email').split('@')[0][:30]
        
        return user
    
    def get_connect_redirect_url(self, request, socialaccount):
        """
        Redireciona após conectar conta social (usuário já existente).
        """
        return '/questoes/index/'
    
    def get_signup_redirect_url(self, request):
        """
        Redireciona após cadastro via rede social.
        """
        return '/questoes/index/'
    
    def respond_user_inactive(self, request, sociallogin):
        """
        Não bloquear usuários inativos - permitir login.
        """
        return None
    
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Permite cadastro automático sem confirmação.
        """
        return True

