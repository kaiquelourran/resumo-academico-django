# 🔍 ANÁLISE DE DEPENDÊNCIAS - PROJETO PHP → DJANGO

## 📊 **HIERARQUIA DE DEPENDÊNCIAS** 

### 🎯 **PÁGINA PRINCIPAL: `questoes/index.php`**

**O QUE ELA USA:**
1. ✅ `conexao.php` → **JÁ MIGRADO** (conexão DB = Django ORM)
2. ✅ `header.php` → Templates Django (`base.html` + `menu_cabecalho.html`)
3. ✅ `footer.php` → Template Django (`base.html` footer)
4. ❌ **Sistema de Notificações** → Novo modelo `RelatorioBug` (JÁ CRIADO!)
5. ❌ **Ranking Semanal** → Query complexa que precisa ser migrada
6. ❌ **Estatísticas do Sistema** → Queries simples que podem ser feitas no Django

**RECURSOS UTILIZADOS:**
- 📊 Estatísticas: Total de assuntos, questões, alternativas
- 🏆 Ranking semanal de usuários
- 🔔 Sistema de notificações
- 🎯 Cards de navegação

---

### 🎯 **PÁGINA: `questoes/escolher_assunto.php`**

**O QUE ELA USA:**
1. ✅ `conexao.php` → **JÁ MIGRADO**
2. ✅ `header.php` → **JÁ MIGRADO**
3. ✅ `footer.php` → **JÁ MIGRADO**
4. ❌ Query de assuntos categorizados → **PRECISA VERIFICAR SE ESTÁ OK**
5. ❌ Busca por nome de assunto → **PODE JÁ ESTAR OK**

**FUNCIONALIDADES:**
- Listagem de assuntos por categoria (Temas, Concursos, Profissionais)
- Busca de assuntos
- Contagem de questões por assunto

---

### 📋 **ARQUIVOS DE CONFIGURAÇÃO**

#### ✅ **`conexao.php`** 
**JÁ MIGRADO** → Django ORM
- Detecta ambiente (local/produção)
- Cria conexão PDO
- Funções de segurança (CSRF, sanitização)
- **MIGRAÇÃO:** Usar `python-dotenv` + configurações do `settings.py`

#### ✅ **`config.php`**
**JÁ MIGRADO** → `settings.py`
- Configurações globais
- Timezone
- Modo desenvolvimento/produção

#### ✅ **`header.php`**
**JÁ MIGRADO** → `questoes/templates/questoes/base.html` + `menu_cabecalho.html`
- Header moderno
- Breadcrumbs
- User info
- Navegação

#### ✅ **`footer.php`**
**JÁ MIGRADO** → `questoes/templates/questoes/base.html` (rodapé)
- Footer moderno
- Links de contato
- Créditos

---

### 🎯 **DEPENDÊNCIAS ENTRE ARQUIVOS**

```
index.php
├── conexao.php ✅ (JÁ MIGRADO)
├── header.php ✅ (JÁ MIGRADO)
├── footer.php ✅ (JÁ MIGRADO)
├── Sistema de Ranking 📊 (NECESSITA MIGRAÇÃO)
│   └── Query complexa de ranking semanal
├── Sistema de Notificações 🔔 (PRECISA COMPLETAR)
│   └── marcar_notificacao_lida.php
│   └── verificar_notificacoes.php
└── Estatísticas 📈 (FÁCIL DE MIGRAR)
    ├── Total assuntos
    ├── Total questões
    └── Total alternativas

escolher_assunto.php
├── conexao.php ✅
├── header.php ✅
└── footer.php ✅
    └── Query assuntos (JÁ FEITO via Django ORM)

quiz_vertical_filtros.php
├── conexao.php ✅
├── header.php ✅
├── footer.php ✅
├── processar_resposta.php (API AJAX) ✅ (JÁ MIGRADO)
└── quiz.js ✅ (JÁ MIGRADO)

resultado_vertical.php
├── conexao.php ✅
├── header.php ✅
└── footer.php ✅

desempenho.php
├── conexao.php ✅
├── header.php ✅
├── footer.php ✅
└── Queries de estatísticas do usuário

relatar_problema.php
├── conexao.php ✅
├── header.php ✅
└── footer.php ✅
```

---

## 🎯 **O QUE FALTA MIGRAR**

### 1️⃣ **Sistema de Ranking Semanal** (index.php)
**ARQUIVO:** `questoes/index.php` (linhas 564-718)
**FUNCIONALIDADE:** 
- Ranking dos top 5 usuários mais ativos na semana
- Posição do usuário atual
- Taxa de acerto

**COMO MIGRAR:**
```python
# Em questoes/views.py
def index_view(request):
    # Estatísticas gerais
    total_assuntos = Assunto.objects.count()
    total_questoes = Questao.objects.count()
    total_alternativas = Alternativa.objects.count()
    
    # Ranking semanal
    from datetime import timedelta
    from django.db.models import Count, Sum
    from django.utils import timezone
    
    inicio_semana = timezone.now() - timedelta(days=7)
    ranking = RespostaUsuario.objects.filter(
        data_resposta__gte=inicio_semana
    ).values('id_usuario').annotate(
        total=Count('id'),
        acertos=Sum('acertou')
    ).order_by('-total', '-acertos')[:5]
```

### 2️⃣ **Sistema de Notificações** (index.php)
**ARQUIVO:** `questoes/index.php` (linhas 25-46)
**FUNCIONALIDADE:**
- Buscar notificações não lidas
- Mostrar badge com contador
- Dropdown com mensagens

**MIGRAÇÃO:** ✅ Já criamos o modelo `RelatorioBug`! Só falta:
- View para buscar notificações
- Endpoint para marcar como lida

### 3️⃣ **API Verificar Notificações**
**ARQUIVO:** `verificar_notificacoes.php`
**COMO MIGRAR:**
```python
@csrf_exempt
def verificar_notificacoes_view(request):
    if request.user.is_authenticated:
        count = RelatorioBug.objects.filter(
            id_usuario=request.user,
            resposta_admin__isnull=False,
            usuario_viu_resposta=False
        ).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})
```

### 4️⃣ **API Marcar Notificação como Lida**
**ARQUIVO:** `marcar_notificacao_lida.php`
**COMO MIGRAR:**
```python
@csrf_exempt
@require_http_methods(["POST"])
def marcar_notificacao_lida_view(request):
    if request.user.is_authenticated:
        id_relatorio = json.loads(request.body).get('id_relatorio')
        try:
            relatorio = RelatorioBug.objects.get(
                id=id_relatorio,
                id_usuario=request.user
            )
            relatorio.usuario_viu_resposta = True
            relatorio.save()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})
```

---

## 📝 **RESUMO DO STATUS**

### ✅ **JÁ MIGRADO E FUNCIONANDO:**
1. ✅ Conexão com banco (Django ORM)
2. ✅ Header e Footer (Templates Django)
3. ✅ Autenticação (login, cadastro, logout)
4. ✅ Escolher assunto
5. ✅ Quiz com validação AJAX
6. ✅ CSS e JavaScript
7. ✅ Media files
8. ✅ Admin panel
9. ✅ Sistema de relatórios (modelo criado)

### 🔄 **PRECISA COMPLETAR:**
1. 🔔 Sistema de notificações (endpoints AJAX)
2. 📊 Ranking semanal (index.php)
3. 📈 Página de desempenho
4. ✅ Dashboard admin customizado

---

## 🚀 **PRÓXIMO PASSO**

**Qual arquivo você quer que eu analise e migre agora?**

1. Completo `index.php` (ranking + notificações) ⭐ RECOMENDADO
2. `escolher_assunto.php` completo (melhorias)
3. `desempenho.php` (estatísticas do usuário)
4. `resultado_vertical.php` (resultado do quiz)

**Sugestão:** Começar com `index.php` completo! 🎯


