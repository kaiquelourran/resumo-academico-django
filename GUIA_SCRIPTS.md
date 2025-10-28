# Guia de Scripts Auxiliares - Django

## 📋 Scripts de Desenvolvimento vs Django Equivalentes

### 🔧 **Scripts PHP que NÃO PRECISAM ser migrados** (Django tem equivalentes nativos)

#### **force_local.php** → Django `settings.py`
- **PHP:** Força configurações locais
- **Django:** Use `DEBUG = True` em `settings.py`
- **Como configurar:**
  ```python
  # settings.py
  DEBUG = True  # Local
  # DEBUG = False  # Produção
  ```

#### **force_online.php** → Django `settings.py`
- **PHP:** Força configurações de produção
- **Django:** Use `DEBUG = False` e variáveis de ambiente
- **Como configurar:**
  ```python
  # settings.py
  import os
  DEBUG = os.environ.get('DEBUG', 'False') == 'True'
  ```

#### **gerar_sql_limpo.php** → Django `dumpdata`
- **PHP:** Gera SQL para migração
- **Django:** Use `python manage.py dumpdata`
- **Comando:**
  ```bash
  python manage.py dumpdata > backup.json
  ```

#### **remover_emojis.php** → Django Management Command
- **PHP:** Remove emojis de arquivos
- **Django:** Crie um management command
- **Como criar:**
  ```python
  # questoes/management/commands/limpar_emojis.py
  from django.core.management.base import BaseCommand
  
  class Command(BaseCommand):
      def handle(self, *args, **options):
          # Lógica para remover emojis
          pass
  ```

---

### 🧪 **Scripts de Teste**

#### **demo_comentarios.html**
- **Status:** ✅ Já migrado (API de comentários implementada)
- **Django:** Views `api_comentarios` já criadas
- **Teste em:** `/questoes/api/comentarios/`

#### **inserir_alternativas_exemplo.php**
- **Status:** ⏳ Não precisa ser migrado
- **Django:** Use fixtures ou admin interface
- **Como usar:**
  ```python
  # Criar fixtures (fixtures/alternativas_exemplo.json)
  python manage.py loaddata alternativas_exemplo
  ```

---

### 📝 **Scripts de Criação de Tabelas → Django Migrations**

#### **criar_tabela_usuarios.php** → Django `User` Model
- **Status:** ✅ **NÃO PRECISA** - Django já tem
- **Django:** Usa modelo `User` nativo
- **Criar migrações:**
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

#### **criar_tabela_comentarios.php** → Model `ComentarioQuestao`
- **Status:** ✅ **JÁ MIGRADO** - Model criado
- **Django:** Model `ComentarioQuestao` em `questoes/models.py`
- **Criar migrações:**
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

#### **criar_tabela_respostas_usuario.php** → Model `RespostaUsuario`
- **Status:** ✅ **JÁ MIGRADO** - Model criado
- **Django:** Model `RespostaUsuario` em `questoes/models.py`
- **Criar migrações:**
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

#### **corrigir_tabela_usuarios.php** → Django Migrations
- **Status:** ✅ **NÃO PRECISA** - Django gerencia automaticamente
- **Django:** Migrations corrigem estrutura automaticamente
- **Como atualizar:**
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

---

## 🛠️ **Django Management Commands Disponíveis**

### Command: `teste_assuntos`
```bash
python manage.py teste_assuntos
```
- **Propósito:** Lista todos os assuntos cadastrados
- **Uso:** Testar estrutura do banco de dados

### Command: `verificar_colunas_concurso`
```bash
python manage.py verificar_colunas_concurso
```
- **Propósito:** Verifica colunas relacionadas a concursos
- **Uso:** Diagnóstico de estrutura

### Command: `verificar_query_direta`
```bash
python manage.py verificar_query_direta
```
- **Propósito:** Executa queries diretas no banco
- **Uso:** Diagnóstico e debugging

---

## 🔄 **Mapeamento PHP → Django**

| Script PHP | Django Equivalente | Status |
|------------|-------------------|--------|
| `force_local.php` | `settings.py` com `DEBUG=True` | ✅ Não precisa migrar |
| `force_online.php` | `settings.py` com `DEBUG=False` | ✅ Não precisa migrar |
| `gerar_sql_limpo.php` | `python manage.py dumpdata` | ✅ Não precisa migrar |
| `remover_emojis.php` | Management command | ⏳ Opcional |
| `demo_comentarios.html` | API `/questoes/api/comentarios/` | ✅ Já migrado |
| `inserir_alternativas_exemplo.php` | Fixtures Django | ⏳ Não essencial |
| `criar_tabela_usuarios.php` | `python manage.py migrate` | ✅ Não precisa |
| `criar_tabela_comentarios.php` | Models já criados | ✅ Já migrado |
| `criar_tabela_respostas_usuario.php` | Models já criados | ✅ Já migrado |
| `corrigir_tabela_usuarios.php` | Migrations automáticas | ✅ Não precisa |

---

## 🚀 **Comandos Django Essenciais**

### 1. Criar Migrações
```bash
python manage.py makemigrations
```

### 2. Aplicar Migrações
```bash
python manage.py migrate
```

### 3. Criar Superusuário
```bash
python manage.py createsuperuser
```

### 4. Fazer Backup (Dados)
```bash
python manage.py dumpdata > backup.json
```

### 5. Restaurar Backup
```bash
python manage.py loaddata backup.json
```

### 6. Coletar Arquivos Estáticos
```bash
python manage.py collectstatic
```

### 7. Executar Servidor de Desenvolvimento
```bash
python manage.py runserver
```

---

## ⚠️ **Scripts de Debug PHP que NÃO PRECISAM ser migrados**

Os seguintes arquivos PHP são apenas para debug e **NÃO PRECISAM** ser migrados:

- ❌ `debug_concursos.php`
- ❌ `debug_escolher_assunto.php`
- ❌ `debug_questao_162.php`
- ❌ `teste_simples.php`
- ❌ `verificar_query_direta.php` (use management command)
- ❌ `verificar_colunas_concurso.php` (use management command)
- ❌ `diagnostico_completo.php` (use migrations e admin interface)

**Motivo:** Django tem ferramentas melhores nativas:
- Django Admin Interface
- Django Debug Toolbar
- Management Commands
- Migrations

---

## 📚 **Documentação Adicional**

### Django Management Commands
- 📖 [COMANDOS_DEBUG.md](COMANDOS_DEBUG.md) - Como usar management commands
- 📖 [CSS_QUIZ.md](CSS_QUIZ.md) - Estilos do sistema
- 📖 [GUIA_CSS.md](GUIA_CSS.md) - Guia de arquivos CSS

### PHP Original
- 📖 [README_SCRIPTS.md](../C:/xampp/htdocs/resumo-quiz/RESUMO%20ACADÊMICO/questoes/README_SCRIPTS.md) - Documentação original

---

## ✅ **Checklist de Migração de Scripts**

- [x] Documentar scripts que NÃO precisam ser migrados
- [x] Mapear scripts PHP → Django
- [x] Criar management commands necessários
- [x] Atualizar documentação
- [ ] Remover scripts PHP de debug (opcional)
- [ ] Criar fixtures de dados de exemplo (opcional)

---

## 🎯 **Resumo**

**Conclusão:** A maioria dos scripts PHP **NÃO PRECISA** ser migrada para Django, pois o Django tem ferramentas nativas melhores para as mesmas funcionalidades:

- ✅ **Migrations** > Scripts de criação de tabelas
- ✅ **Management Commands** > Scripts de manutenção
- ✅ **dumpdata** > Scripts de backup SQL
- ✅ **Fixtures** > Scripts de inserção de dados
- ✅ **Admin Interface** > Scripts de debug

**Recomendação:** Focus em migrar apenas a **lógica de negócio** (views, models, templates), não os scripts auxiliares.

