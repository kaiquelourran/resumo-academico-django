# 🔧 Corrigir Erro: ModuleNotFoundError: No module named 'import_export'

## ⚠️ Problema

O erro `ModuleNotFoundError: No module named 'import_export'` ocorre porque o `django-import-export` não está instalado no container Docker.

## ✅ Solução

### Opção 1: Reconstruir o Container Docker (Recomendado)

Se você está usando Docker Compose, reconstrua o container:

```bash
# Parar os containers
docker-compose down

# Reconstruir a imagem Docker (força a reinstalação de todas as dependências)
docker-compose build --no-cache

# Iniciar os containers novamente
docker-compose up
```

### Opção 2: Instalar Manualmente no Container

Se você quiser instalar apenas no container em execução:

```bash
# Entrar no container
docker-compose exec web bash

# Instalar django-import-export
pip install django-import-export==4.0.0

# Sair do container
exit

# Reiniciar o container
docker-compose restart web
```

### Opção 3: Usar Ambiente Local (Sem Docker)

Se você não estiver usando Docker, instale no ambiente virtual local:

```bash
# Ativar o ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar django-import-export
pip install django-import-export==4.0.0

# Verificar se foi instalado
pip list | findstr import
```

## 📋 Verificação

Após reconstruir/instalar, verifique:

```bash
# No container Docker
docker-compose exec web pip list | grep import

# Ou no ambiente local
pip list | findstr import
```

Deve mostrar:
```
django-import-export    4.0.0
```

## 🔍 Verificar se está no requirements.txt

O `requirements.txt` já contém:
```
django-import-export==4.0.0
```

## ✅ Status

- ✅ `requirements.txt` contém `django-import-export==4.0.0`
- ✅ `settings.py` tem `'import_export'` em `INSTALLED_APPS`
- ⚠️ **PRECISA**: Reconstruir o container Docker para instalar as dependências

## 🎯 Comando Rápido (Docker Compose)

```bash
docker-compose down && docker-compose build --no-cache && docker-compose up
```

Isso vai:
1. Parar os containers
2. Reconstruir a imagem Docker (instalando todas as dependências do requirements.txt)
3. Iniciar os containers novamente

