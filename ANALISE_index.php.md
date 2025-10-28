# 📋 ANÁLISE COMPLETA: `questoes/index.php`

## 📊 **ESTRUTURA GERAL**

Arquivo principal do dashboard de questões do sistema PHP.
- **Localização:** `C:\xampp\htdocs\resumo-quiz\RESUMO ACADÊMICO\questoes\index.php`
- **Linhas totais:** 1.189 linhas
- **Funcionalidade:** Dashboard principal com estatísticas, ranking semanal e notificações

---

## 🎯 **FUNCIONALIDADES PRINCIPAIS**

### 1. **SISTEMA DE AUTENTICAÇÃO E SEGURANÇA** (Linhas 1-23)
```php
✅ Verificação de sessão (logged_in)
✅ Token CSRF 
✅ Headers de segurança
✅ Redirecionamento para login se não autenticado
```

**MIGRAÇÃO:** ✅ Já implementado via Django decorators

---

### 2. **SISTEMA DE NOTIFICAÇÕES** (Linhas 25-46)
```php
📋 Query busca notificações não lidas
📋 Busca em: tabela 'relatorios_bugs'
📋 Filtros:
   - id_usuario = usuário atual
   - resposta_admin IS NOT NULL
   - resposta_admin != ''
   - usuario_viu_resposta = FALSE
📋 Ordenação: data_atualizacao DESC
📋 Limite: 5 notificações
```

**ESTRUTURA DA NOTIFICAÇÃO:**
- `id_relatorio`
- `titulo`
- `resposta_admin`
- `data_atualizacao`
- `status`
- `prioridade`

**MIGRAÇÃO:** ✅ Modelo `RelatorioBug` já criado! Falta apenas implementar os endpoints AJAX.

---

### 3. **ESTATÍSTICAS DO SISTEMA** (Linhas 532-562)
```php
📊 Total de Assuntos (COUNT assuntos)
📊 Total de Questões (COUNT questoes)
📊 Total de Alternativas (COUNT alternativas)
```

**MIGRAÇÃO:** FÁCIL - Apenas usar Django ORM count()

---

### 4. **RANKING SEMANAL** (Linhas 564-718) ⭐ COMPLEXO

#### 4.1 **Detecção de Tabelas** (Linhas 568-635)
```php
🔍 Verifica 2 possíveis tabelas:
   1. respostas_usuarios (id_usuario)
   2. respostas_usuario (user_id)

🔍 Para cada tabela:
   - Verifica se existe
   - Verifica se tem dados na semana
   - Adiciona query à lista de sources
```

**LÓGICA DE SEMANA:**
```sql
DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY) 
-- Início da semana (segunda-feira)
DATE_ADD(DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY), INTERVAL 7 DAY)
-- Fim da semana (domingo)
```

#### 4.2 **Query de Ranking** (Linhas 659-668)
```sql
SELECT 
    COALESCE(u.id_usuario, x.id_usuario) AS id_usuario,
    COALESCE(u.nome, 'Anônimo') AS nome,
    COUNT(*) AS total,
    SUM(CASE WHEN x.acertou = 1 THEN 1 ELSE 0 END) AS acertos
FROM (UNION queries) x
LEFT JOIN usuarios u ON u.id_usuario = x.id_usuario
GROUP BY id_usuario, nome
ORDER BY total DESC, acertos DESC, nome ASC
LIMIT 5
```

**RESULTADO:**
- Top 5 usuários
- Nome, total de respostas, total de acertos

#### 4.3 **Posição do Usuário Atual** (Linhas 679-710)
```sql
-- Query completa SEM LIMIT para achar posição
-- Procura usuário atual no ranking
-- Retorna: posição, total_respostas, total_acertos
```

**MIGRAÇÃO:** Complexo mas viável com Django ORM.

---

### 5. **CARDS DE NAVEGAÇÃO** (Linhas 872-900)

**Cards sempre visíveis:**
1. 🎯 **Fazer Questões** → `escolher_assunto.php`
2. 🐛 **Relatar Problema** → `relatar_problema.php`

**Cards para ADMIN:**
3. 📋 **Gerenciar Questões** → `gerenciar_questoes_sem_auth.php`

---

### 6. **ÁREA ADMINISTRATIVA** (Linhas 902-941)

**Visível apenas para admins** (`$_SESSION['user_type'] === 'admin'`)

**Cards Admin:**
1. 👨‍💼 Dashboard Admin → `admin/dashboard.php`
2. 📝 Adicionar Conteúdo → `admin/add_assunto.php`
3. ❓ Adicionar Questão → `admin/add_questao.php`
4. 🐛 Gerenciar Relatórios → `admin/gerenciar_relatorios.php`

---

### 7. **RANKING DUPLICADO** (Linhas 943-1001)

⚠️ **OBSERVAÇÃO:** O ranking aparece 2 vezes no código (uma duplicação não intencional).

---

## 🔧 **DEPENDÊNCIAS EXTERNAS**

### **Includes:**
1. ✅ `conexao.php` - Conexão DB
2. ✅ `header.php` - Header com breadcrumb
3. ✅ `footer.php` - Footer moderno

### **Endpoints AJAX:**
1. ❌ `marcar_notificacao_lida.php` - Marcar notificação como lida
2. ❌ `verificar_notificacoes.php` - Auto-refresh (30s)

### **Dependências de Páginas:**
- `escolher_assunto.php`
- `relatar_problema.php`
- `admin/dashboard.php`
- `admin/add_assunto.php`
- `admin/add_questao.php`
- `admin/gerenciar_relatorios.php`
- `admin/gerenciar_questoes_sem_auth.php`

---

## 📝 **ANÁLISE DO HTML/CSS/JAVASCRIPT**

### **CSS Importado:**
- `modern-style.css` - Estilos modernos

### **CSS Inline (Linhas 57-482):**
- Estilos de cards, ranking, notificações
- Responsividade mobile

### **JavaScript (Linhas 1004-1187):**

**1. Garantir botão "Sair"** (Linhas 1005-1096)
- Adiciona botão logout no header
- Mostra perfil do usuário
- Adiciona botão "Ir para o Site"

**2. Cards clicáveis** (Linhas 1098-1118)
- Torna cards navegáveis
- Adiciona efeitos hover/click

**3. Mover ranking acima do footer** (Linhas 1120-1137)
- Manipula DOM para reposicionar

**4. Sistema de notificações** (Linhas 1139-1187)
- Toggle dropdown
- Marcar notificação como lida (AJAX)
- Auto-refresh a cada 30s

---

## 🚀 **PLANO DE MIGRAÇÃO**

### ✅ **JÁ MIGRADO:**
1. ✅ Autenticação (Django auth)
2. ✅ Modelo RelatorioBug
3. ✅ Estatísticas simples (count)

### 🔄 **PRECISA MIGRAR:**

#### 1️⃣ **Sistema de Notificações**
```python
# Views necessárias:
- notificacoes_view() - Buscar notificações
- marcar_lida_view() - Marcar como lida (AJAX)
- verificar_notificacoes_view() - Auto-refresh (AJAX)
```

#### 2️⃣ **Ranking Semanal**
```python
# Query complexa com Django ORM:
from datetime import timedelta
from django.utils import timezone

inicio_semana = timezone.now() - timedelta(days=7)
ranking = RespostaUsuario.objects.filter(
    data_resposta__gte=inicio_semana
).values('id_usuario').annotate(
    total=Count('id'),
    acertos=Sum('acertou')
).order_by('-total', '-acertos')[:5]
```

#### 3️⃣ **Cards e Área Admin**
- Templates para cards
- Lógica de verificação admin
- Links para áreas admin

#### 4️⃣ **JavaScript**
- Adaptar para Django URLs
- AJAX endpoints
- Auto-refresh

---

## 📊 **ESTRUTURA DE DADOS NECESSÁRIAS**

### **Queries SQL usadas:**
1. `SELECT COUNT(*) FROM assuntos`
2. `SELECT COUNT(*) FROM questoes`
3. `SELECT COUNT(*) FROM alternativas`
4. `SELECT ... FROM relatorios_bugs WHERE ...` (notificações)
5. `SELECT ... FROM respostas_usuarios/respostas_usuario` (ranking)

### **Tabelas acessadas:**
- `assuntos`
- `questoes`
- `alternativas`
- `relatorios_bugs`
- `respostas_usuarios` ou `respostas_usuario`
- `usuarios`

---

## 🎯 **CONCLUSÃO**

**Arquivo complexo mas migrável!**

- **Funções principais:** 3 (Notificações, Estatísticas, Ranking)
- **Queries SQL:** 5
- **AJAX endpoints:** 2
- **Includes:** 3
- **JavaScript:** 4 blocos

**Pronto para implementação quando você solicitar!** ✅


