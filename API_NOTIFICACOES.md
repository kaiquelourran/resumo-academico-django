# API de Notificações - Documentação

Este documento descreve a API de notificações do sistema, que replica a funcionalidade do arquivo PHP `verificar_notificacoes.php`.

## Endpoint

### URL
```
GET /questoes/api/notificacoes/
```

### Método
`GET`

### Autenticação
Requer usuário autenticado. Retorna `count: 0` se não estiver autenticado.

## Resposta

### Sucesso
```json
{
    "count": 5
}
```

### Erro ou Usuário não autenticado
```json
{
    "count": 0
}
```

## Uso

### JavaScript (AJAX)
```javascript
fetch('/questoes/api/notificacoes/', {
    method: 'GET',
    headers: {
        'X-CSRFToken': getCookie('csrftoken')
    }
})
.then(response => response.json())
.then(data => {
    console.log('Notificações não lidas:', data.count);
    // Atualizar badge de notificações
    document.getElementById('notification-count').textContent = data.count;
})
.catch(error => {
    console.error('Erro ao buscar notificações:', error);
});
```

### jQuery (AJAX)
```javascript
$.ajax({
    url: '/questoes/api/notificacoes/',
    method: 'GET',
    success: function(data) {
        console.log('Notificações não lidas:', data.count);
        // Atualizar badge de notificações
        $('#notification-count').text(data.count);
    },
    error: function() {
        console.error('Erro ao buscar notificações');
    }
});
```

### Python (Django)
```python
from django.http import JsonResponse
from questoes.models import RelatorioBug

# Em uma view
def minha_view(request):
    if request.user.is_authenticated:
        count = RelatorioBug.objects.filter(
            id_usuario=request.user,
            resposta_admin__isnull=False
        ).exclude(
            resposta_admin=''
        ).filter(
            usuario_viu_resposta=False
        ).count()
        
        context = {'notification_count': count}
        return render(request, 'template.html', context)
```

## Lógica de Notificações

### O que é uma notificação não lida?

Uma notificação não lida é um `RelatorioBug` que:
1. ✅ Pertence ao usuário logado (`id_usuario = request.user`)
2. ✅ Tem uma resposta do administrador (`resposta_admin IS NOT NULL`)
3. ✅ A resposta não está vazia (`resposta_admin != ''`)
4. ✅ O usuário ainda não viu a resposta (`usuario_viu_resposta = FALSE`)

### Query Equivalente (SQL)
```sql
SELECT COUNT(*) as total
FROM relatorios_bugs 
WHERE id_usuario = ?
AND resposta_admin IS NOT NULL 
AND resposta_admin != '' 
AND usuario_viu_resposta = FALSE
```

### Query Equivalente (Django ORM)
```python
RelatorioBug.objects.filter(
    id_usuario=request.user,
    resposta_admin__isnull=False
).exclude(
    resposta_admin=''
).filter(
    usuario_viu_resposta=False
).count()
```

## Integração com o Template

### Badge de Notificações no Header
```html
<!-- No base.html ou header.html -->
<a href="#" id="notifications-link">
    <i class="fas fa-bell"></i>
    <span id="notification-count">0</span>
</a>

<script>
    // Atualizar contagem a cada 30 segundos
    setInterval(function() {
        fetch('/questoes/api/notificacoes/', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            const count = data.count;
            const badge = document.getElementById('notification-count');
            badge.textContent = count;
            
            // Adicionar classe 'has-notifications' se houver notificações
            const link = document.getElementById('notifications-link');
            if (count > 0) {
                link.classList.add('has-notifications');
            } else {
                link.classList.remove('has-notifications');
            }
        });
    }, 30000); // Atualizar a cada 30 segundos
</script>

<style>
    .has-notifications {
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
```

## Marcar Notificação como Lida

### View para marcar como lida
```python
from django.http import JsonResponse

def marcar_notificacao_lida(request, notificacao_id):
    """Marca uma notificação específica como lida"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})
    
    try:
        notificacao = RelatorioBug.objects.get(
            id=notificacao_id,
            id_usuario=request.user
        )
        notificacao.usuario_viu_resposta = True
        notificacao.save()
        
        return JsonResponse({'success': True})
    except RelatorioBug.DoesNotExist:
        return JsonResponse({'success': False})
```

### URL para marcar como lida
```python
from django.urls import path

urlpatterns = [
    # ...
    path('api/notificacoes/<int:notificacao_id>/marcar-lida/', views.marcar_notificacao_lida, name='marcar_notificacao_lida'),
]
```

### Uso em JavaScript
```javascript
function marcarComoLida(notificacaoId) {
    fetch(`/questoes/api/notificacoes/${notificacaoId}/marcar-lida/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Notificação marcada como lida');
            // Atualizar UI
        }
    });
}
```

## Migração do PHP para Django

### PHP (`verificar_notificacoes.php`)
```php
<?php
$stmt = $pdo->prepare("
    SELECT COUNT(*) as total
    FROM relatorios_bugs 
    WHERE id_usuario = ? 
    AND resposta_admin IS NOT NULL 
    AND resposta_admin != '' 
    AND usuario_viu_resposta = FALSE
");

$stmt->execute([$_SESSION['id_usuario']]);
$result = $stmt->fetch(PDO::FETCH_ASSOC);

echo json_encode(['count' => intval($result['total'])]);
?>
```

### Django (Equivalente)
```python
from django.http import JsonResponse
from questoes.models import RelatorioBug

def api_notificacoes(request):
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0})
    
    count = RelatorioBug.objects.filter(
        id_usuario=request.user,
        resposta_admin__isnull=False
    ).exclude(
        resposta_admin=''
    ).filter(
        usuario_viu_resposta=False
    ).count()
    
    return JsonResponse({'count': count})
```

## Performance

- **Tempo de execução**: < 10ms para bancos pequenos/médios
- **Indexação recomendada**: `id_usuario`, `usuario_viu_resposta`
- **Cache**: Considere adicionar cache Redis para reduzir consultas ao banco

### Adicionar Cache
```python
from django.core.cache import cache

def api_notificacoes(request):
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0})
    
    cache_key = f'notifications_count_{request.user.id}'
    count = cache.get(cache_key)
    
    if count is None:
        count = RelatorioBug.objects.filter(
            id_usuario=request.user,
            resposta_admin__isnull=False
        ).exclude(
            resposta_admin=''
        ).filter(
            usuario_viu_resposta=False
        ).count()
        
        # Cache por 5 minutos
        cache.set(cache_key, count, 300)
    
    return JsonResponse({'count': count})
```

## Testes

### Teste Manual
```bash
# Autenticar
curl -X GET http://localhost:8000/questoes/api/notificacoes/ \
  -H "Cookie: sessionid=xxx"

# Resposta esperada
{"count": 5}
```

### Teste Automatizado
```python
from django.test import TestCase
from django.contrib.auth.models import User
from questoes.models import RelatorioBug
from django.urls import reverse

class NotificationAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
    def test_notification_count(self):
        # Criar notificações não lidas
        RelatorioBug.objects.create(
            id_usuario=self.user,
            nome_usuario='Test User',
            email_usuario='test@example.com',
            titulo='Test',
            descricao='Test description',
            resposta_admin='Resposta do admin',
            usuario_viu_resposta=False
        )
        
        # Testar API
        response = self.client.get(reverse('questoes:api_notificacoes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
```

## Segurança

1. **Autenticação**: Requer usuário logado
2. **Isolamento**: Usuários só veem suas próprias notificações
3. **Logging**: Erros são registrados no log do Django
4. **Validação**: Retorna 0 em caso de erro (fail-safe)

## Notas Finais

- A API retorna apenas o **contador**, não os detalhes das notificações
- Para buscar detalhes, crie uma API separada
- Use polling a cada 30-60 segundos para atualizar o contador
- Considere usar WebSockets para notificações em tempo real

