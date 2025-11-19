# 🐳 Guia de Uso Docker - Resumo Acadêmico

## 📋 Arquivos Criados

✅ **Dockerfile** - Imagem otimizada multi-stage para Django  
✅ **compose.yml** - Configuração completa Docker Compose v2  
✅ **docker-entrypoint.sh** - Script de inicialização automática  
✅ **.env.example** - Exemplo de variáveis de ambiente  

## 🚀 Como Usar

### 1. Preparação Inicial

```bash
# 1. Copiar arquivo de variáveis de ambiente
cp .env.example .env

# 2. Editar .env com suas configurações (opcional)
# As configurações padrão já funcionam para desenvolvimento
```

### 2. Construir e Iniciar os Containers

```bash
# Usar o novo compose.yml (recomendado)
docker compose -f compose.yml up --build

# OU usar docker-compose.yml antigo (ainda funciona)
docker-compose up --build
```

### 3. Acessar a Aplicação

- **Aplicação Django**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Superusuário padrão** (criado automaticamente em DEBUG=True):
  - Email: `admin@resumoacademico.com`
  - Senha: `admin123`

### 4. Comandos Úteis

```bash
# Ver logs
docker compose -f compose.yml logs -f

# Parar containers
docker compose -f compose.yml down

# Parar e remover volumes (CUIDADO: apaga dados!)
docker compose -f compose.yml down -v

# Reconstruir apenas o serviço web
docker compose -f compose.yml up --build web

# Executar comandos Django dentro do container
docker compose -f compose.yml exec web python manage.py createsuperuser
docker compose -f compose.yml exec web python manage.py migrate
docker compose -f compose.yml exec web python manage.py collectstatic

# Acessar shell do container
docker compose -f compose.yml exec web bash

# Acessar PostgreSQL
docker compose -f compose.yml exec db psql -U resumo_user -d resumo_academico_db
```

## 🔧 Configurações

### Variáveis de Ambiente

As variáveis podem ser definidas no arquivo `.env` ou diretamente no `compose.yml`:

- `SECRET_KEY` - Chave secreta do Django
- `DEBUG` - Modo debug (True/False)
- `ALLOWED_HOSTS` - Hosts permitidos (separados por vírgula)
- `POSTGRES_DB` - Nome do banco de dados
- `POSTGRES_USER` - Usuário do PostgreSQL
- `POSTGRES_PASSWORD` - Senha do PostgreSQL
- `POSTGRES_HOST` - Host do PostgreSQL (use `db` no Docker)
- `POSTGRES_PORT` - Porta do PostgreSQL (5432)

### Volumes

- **postgres_data** - Dados persistentes do PostgreSQL
- **static_volume** - Arquivos estáticos coletados
- **media_volume** - Arquivos de mídia (uploads)

## 🔒 Segurança

### Desenvolvimento
- DEBUG=True (padrão)
- Senhas padrão (alterar em produção!)
- Portas expostas localmente

### Produção
⚠️ **IMPORTANTE**: Antes de usar em produção:

1. Alterar `DEBUG=False` no `.env`
2. Gerar nova `SECRET_KEY`:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
3. Alterar senhas do PostgreSQL
4. Configurar `ALLOWED_HOSTS` com seu domínio
5. Usar servidor web (Nginx/Apache) como proxy reverso
6. Configurar HTTPS/SSL

## 📦 O que o Script de Inicialização Faz

O `docker-entrypoint.sh` executa automaticamente:

1. ✅ Aguarda PostgreSQL estar pronto
2. ✅ Executa migrations (`python manage.py migrate`)
3. ✅ Coleta arquivos estáticos (`python manage.py collectstatic`)
4. ✅ Cria superusuário padrão (apenas em DEBUG=True)

## 🐛 Troubleshooting

### Erro: "Cannot connect to database"
- Verifique se o serviço `db` está rodando: `docker compose ps`
- Verifique as variáveis de ambiente no `.env`

### Erro: "Port already in use"
- Altere a porta no `compose.yml` ou `.env`:
  ```yaml
  ports:
    - "8001:8000"  # Usa porta 8001 no host
  ```

### Erro: "Permission denied" no docker-entrypoint.sh
- O script já tem permissões corretas, mas se necessário:
  ```bash
  chmod +x docker-entrypoint.sh
  ```

### Limpar tudo e começar do zero
```bash
# Parar e remover tudo
docker compose -f compose.yml down -v

# Remover imagens
docker rmi resumo-academico-web

# Reconstruir do zero
docker compose -f compose.yml up --build
```

## 📝 Notas

- O `compose.yml` é mais completo que o `docker-compose.yml` antigo
- Ambos funcionam, mas recomendo usar `compose.yml`
- Os dados do PostgreSQL são persistidos em volumes Docker
- Arquivos de mídia e estáticos também são persistidos

## 🔄 Migração do docker-compose.yml Antigo

Se você estava usando o `docker-compose.yml` antigo:

1. Os volumes e dados são compatíveis
2. Pode continuar usando o antigo ou migrar para o novo
3. O novo `compose.yml` tem mais recursos:
   - Healthchecks
   - Melhor organização
   - Script de inicialização automática
   - Configurações mais robustas

