"""
Backend de autenticação customizado para suportar hashes de senha do PHP (bcrypt)
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
import bcrypt


class PHPPasswordBackend(ModelBackend):
    """
    Backend que suporta hashes de senha do PHP (password_hash/password_verify)
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            # Buscar usuário pelo username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        # Verificar se a senha é um hash do PHP (bcrypt)
        if user.password.startswith('$2y$') or user.password.startswith('$2b$') or user.password.startswith('$2a$'):
            # Hash do PHP - usar bcrypt
            password_bytes = password.encode('utf-8')
            # Converter $2y$ para $2b$ (compatível com bcrypt Python)
            hash_to_check = user.password.replace('$2y$', '$2b$').encode('utf-8')
            
            try:
                if bcrypt.checkpw(password_bytes, hash_to_check):
                    return user
            except Exception as e:
                print(f"Erro ao verificar senha bcrypt: {e}")
                return None
        else:
            # Hash do Django - usar método padrão
            if user.check_password(password):
                return user
        
        return None


