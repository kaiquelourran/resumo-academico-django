# Configuração de Segurança - Headers HTTP

Este documento descreve como configurar os headers de segurança no servidor web para replicar as funcionalidades do arquivo PHP `security_headers.php`.

## Headers Configurados via Django

Os seguintes headers são configurados automaticamente pelo Django via `settings.py` e `middleware.py`:

- `X-Content-Type-Options: nosniff` - Previne MIME sniffing
- `X-Frame-Options: SAMEORIGIN` - Protege contra clickjacking  
- `Referrer-Policy: strict-origin-when-cross-origin` - Controla informações de referrer
- `Permissions-Policy: geolocation=(), microphone=(), camera=()` - Controla features do navegador

## Headers Adicionais (Configurar no Servidor Web)

### 1. Content Security Policy (CSP)

**Para Nginx:**

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.googletagmanager.com https://pagead2.googlesyndication.com https://accounts.google.com https://apis.google.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://www.google-analytics.com https://accounts.google.com; frame-src 'self' https://accounts.google.com" always;
```

**Para Apache (.htaccess):**

```apache
Header set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.googletagmanager.com https://pagead2.googlesyndication.com https://accounts.google.com https://apis.google.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://www.google-analytics.com https://accounts.google.com; frame-src 'self' https://accounts.google.com"
```

### 2. Strict-Transport-Security (HSTS) - Apenas para HTTPS

**Para Nginx:**

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

**Para Apache (.htaccess):**

```apache
Header set Strict-Transport-Security "max-age=31536000; includeSubDomains"
```

**⚠️ IMPORTANTE:** Configure HSTS apenas se o site estiver usando HTTPS. Não configure em desenvolvimento local.

## Resumo das Configurações

### Configurado via Django
- ✅ X-Content-Type-Options
- ✅ X-Frame-Options  
- ✅ Referrer-Policy
- ✅ Permissions-Policy
- ✅ CSRF Protection
- ✅ Session Security

### Configurar no Servidor Web
- ⚠️ Content-Security-Policy (CSP)
- ⚠️ Strict-Transport-Security (HSTS) - Apenas com HTTPS

## Migração do PHP para Django

### PHP (`security_headers.php`):
```php
header('Content-Security-Policy: default-src...');
header('X-Content-Type-Options: nosniff');
// etc...
```

### Django (`settings.py` + `middleware.py`):
```python
# Configurações automáticas via settings.py
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
# etc...

# Middleware adiciona headers customizados
class SecurityHeadersMiddleware:
    def __call__(self, request):
        response['Permissions-Policy'] = '...'
        return response
```

## Modo de Produção

Quando subir para produção na Hostinger:

1. **Ative HTTPS** se ainda não estiver ativo
2. **Configure os headers adicionais** (CSP e HSTS) no painel de configuração do servidor web
3. **Ative as configurações seguras** em `settings.py`:
   ```python
   DEBUG = False
   CSRF_COOKIE_SECURE = True
   SESSION_COOKIE_SECURE = True
   SECURE_HSTS_SECONDS = 31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   ```

## Notas

- **X-XSS-Protection foi removido** do PHP original pois está obsoleto. Navegadores modernos usam Content-Security-Policy
- Os headers configurados via Django são aplicados automaticamente em todas as respostas
- Headers adicionais como CSP e HSTS devem ser configurados no servidor web para melhor performance

