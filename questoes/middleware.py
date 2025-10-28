"""
Middleware personalizado para adicionar headers de segurança adicionais
"""

class SecurityHeadersMiddleware:
    """
    Middleware para adicionar headers de segurança modernos
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Permissions-Policy - Controla features do navegador
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response
    

