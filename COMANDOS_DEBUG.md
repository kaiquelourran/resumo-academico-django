# Comandos de Debug - Debug do Sistema

Este documento descreve os comandos de debug disponíveis para testar o sistema.

## Comando de Teste de Assuntos

### PHP (Original)
```php
php teste_simples.php
```

### Django (Equivalente)
```bash
python manage.py teste_assuntos
```

### O que o comando faz?

O comando `teste_assuntos` lista todos os assuntos do banco de dados, organizados por tipo:
- ✅ **Temas**: Categoria padrão
- 🏆 **Concursos**: Assuntos de concursos públicos
- 💼 **Profissionais**: Assuntos profissionais/carreiras

### Saída Esperada

```
🧪 TESTE SIMPLES - FORÇA BRUTA
==================================================

📊 TODOS OS ASSUNTOS:
--------------------------------------------------------------------------------
ID    Nome                                      Tipo
--------------------------------------------------------------------------------
1     Matemática                               tema
2     Português                                tema
3     Concurso MPF 2023                        concurso
4     Concurso TRT                             concurso
5     Profissão Terapeuta                      profissional

📈 CONTAGEM:
Temas: 2
Concursos: 2
Profissionais: 1

✅ CONCURSOS ENCONTRADOS! O problema NÃO é no banco de dados.
```

## Configuração do Ambiente

Para executar o comando, você precisa:

### 1. Ativar o ambiente virtual
```bash
# No Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# No Windows (CMD)
venv\Scripts\activate.bat

# No Linux/Mac
source venv/bin/activate
```

### 2. Verificar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Executar o comando
```bash
python manage.py teste_assuntos
```

## Debugging de Assuntos

### Verificar estrutura do banco
```bash
python manage.py dbshell
```

No shell do banco:
```sql
SELECT id, nome, tipo_assunto FROM assuntos ORDER BY tipo_assunto, nome;
```

### Verificar dados
```bash
python manage.py shell
```

No shell Python:
```python
from questoes.models import Assunto

# Contar por tipo
assuntos = Assunto.objects.all()
temas = assuntos.filter(tipo_assunto='tema').count()
concursos = assuntos.filter(tipo_assunto='concurso').count()
profissionais = assuntos.filter(tipo_assunto='profissional').count()

print(f"Temas: {temas}")
print(f"Concursos: {concursos}")
print(f"Profissionais: {profissionais}")
```

## Migração do PHP para Django

### PHP (`teste_simples.php`)
```php
<?php
$sql = "SELECT a.id_assunto, a.nome, a.tipo_assunto 
        FROM assuntos a 
        ORDER BY a.tipo_assunto, a.nome";
$result = $pdo->query($sql)->fetchAll(PDO::FETCH_ASSOC);

foreach ($result as $r) {
    echo "<tr>";
    echo "<td>" . htmlspecialchars($r['id_assunto']) . "</td>";
    echo "<td>" . htmlspecialchars($r['nome']) . "</td>";
    echo "<td>" . htmlspecialchars($r['tipo_assunto']) . "</td>";
    echo "</tr>";
}
?>
```

### Django (Equivalente)
```python
from questoes.models import Assunto

assuntos = Assunto.objects.all().order_by('tipo_assunto', 'nome')

for assunto in assuntos:
    print(f"{assunto.id} | {assunto.nome} | {assunto.tipo_assunto}")
```

## Verificação de Colunas de Concurso

### PHP (Original)
```php
php verificar_colunas_concurso.php
```

### Django (Equivalente)
```bash
python manage.py verificar_colunas_concurso
```

### O que o comando faz?

O comando `verificar_colunas_concurso` verifica se as colunas de concurso existem na tabela de assuntos:
- ✅ Verifica se as colunas `concurso_ano`, `concurso_banca`, `concurso_orgao`, `concurso_prova` existem
- 🔧 Sugere criar migrações se faltam colunas
- 📊 Lista todos os concursos existentes
- 🎯 Mostra informações de cada concurso (ano, banca, órgão, prova)

### Saída Esperada

```
🔍 VERIFICAÇÃO DE COLUNAS DE CONCURSO
==================================================

1. Estrutura atual da tabela 'assuntos':
--------------------------------------------------------------------------------
Campo                Tipo                 Null       Key        Extra
--------------------------------------------------------------------------------
id                   bigint(20)           NO         PRI        auto_increment
nome                 varchar(200)          NO
tipo_assunto         varchar(20)           YES
concurso_ano         varchar(10)           YES
concurso_banca       varchar(100)          YES
concurso_orgao       varchar(100)          YES
concurso_prova       varchar(100)          YES

2. Verificação das colunas de concurso:
✅ Coluna 'concurso_ano' existe
✅ Coluna 'concurso_banca' existe
✅ Coluna 'concurso_orgao' existe
✅ Coluna 'concurso_prova' existe

3. Adicionar colunas faltantes (se necessário):
✅ Todas as colunas de concurso já existem!

4. Assuntos de concurso existentes:
Encontrados 5 concursos:
--------------------------------------------------------------------------------
ID    Nome                          Ano        Banca                   Órgão                 Prova
--------------------------------------------------------------------------------
1     Concurso TRT-SP 2023          2023       FCC                    TRT-SP                Prova de Juiz
2     Concurso MPF 2022             2022       CESPE                  MPF                    Prova de Analista
```

### Corrigir Estrutura do Banco

Se faltam colunas, execute as migrações:

```bash
# Criar migrations
python manage.py makemigrations questoes

# Aplicar migrations
python manage.py migrate
```

## Verificação Direta da Query

### PHP (Original)
```php
php verificar_query_direta.php
```

### Django (Equivalente)
```bash
python manage.py verificar_query_direta
```

### O que o comando faz?

O comando `verificar_query_direta` executa múltiplas verificações no banco de dados:
- ✅ Executa a query exata do `escolher_assunto` (com LEFT JOIN + GROUP BY)
- 🔍 Verifica se um ID específico existe na tabela assuntos
- 📊 Lista todos os IDs da tabela assuntos
- 🔄 Compara query com agregação vs sem agregação
- 📝 Verifica questões associadas a um assunto específico
- 🎯 Diagnóstico final com contagem por tipo

### Saída Esperada

```
🔍 VERIFICAÇÃO DIRETA DA QUERY
================================================================================

1. Query EXATA (do escolher_assunto):
--------------------------------------------------------------------------------
SQL equivalente (ORM):
  Assunto.objects.annotate(total_questoes=Count("questoes"))
--------------------------------------------------------------------------------
ID    Nome                                      tipo_assunto        Questões 
--------------------------------------------------------------------------------
1     Matemática                               tema                10
2     Concurso TRT-SP 2023                     concurso            5
3     Português                                tema                8

Total de linhas retornadas: 3

2. Verificação Direta do ID (escolha um ID):
--------------------------------------------------------------------------------
Verificando ID 2:
✅ ID 2 EXISTE na tabela assuntos
Nome: Concurso TRT-SP 2023
Tipo: concurso
Questões: 5

3. TODOS os IDs da Tabela 'assuntos':
--------------------------------------------------------------------------------
ID    Nome                                      tipo_assunto
--------------------------------------------------------------------------------
1     Matemática                               tema
2     Concurso TRT-SP 2023                     concurso
3     Português                                tema

4. Query SEM Agregação (para comparar):
--------------------------------------------------------------------------------
ID    Nome                                      tipo_assunto
--------------------------------------------------------------------------------
1     Matemática                               tema
3     Português                                tema
2     Concurso TRT-SP 2023                     concurso

Total de linhas retornadas: 3

5. Questões Associadas (primeiro assunto com questões):
--------------------------------------------------------------------------------
✅ Questões encontradas para ID 2: 5
ID         Enunciado                                        ID Assunto     
--------------------------------------------------------------------------------
1          Questão sobre direito do trabalho...            2

6. 🎯 DIAGNÓSTICO FINAL:
--------------------------------------------------------------------------------
Temas: 2
Concursos: 1
Profissionais: 0

✅ 1 concurso(s) encontrado(s) corretamente na query!
```

### Quando usar?

- Quando concursos não aparecem na listagem
- Para verificar se a query está retornando dados corretos
- Para debug de problemas com GROUP BY
- Para verificar integridade dos dados

## Outros Comandos Úteis

### Criar um assunto de teste
```bash
python manage.py shell
```

```python
from questoes.models import Assunto

# Criar um concurso
Assunto.objects.create(
    nome='Concurso TRT-SP 2023',
    tipo_assunto='concurso',
    concurso_ano='2023',
    concurso_banca='FCC',
    concurso_orgao='TRT-SP'
)

# Criar um tema
Assunto.objects.create(
    nome='Matemática Básica',
    tipo_assunto='tema'
)

# Criar um profissional
Assunto.objects.create(
    nome='Gestão de Carreiras',
    tipo_assunto='profissional'
)
```

### Listar todos os assuntos
```bash
python manage.py shell
```

```python
from questoes.models import Assunto

print("\n".join([
    f"{a.id} - {a.nome} ({a.tipo_assunto})" 
    for a in Assunto.objects.all()
]))
```

### Limpar e recriar banco (CUIDADO!)
```bash
# ⚠️ ATENÇÃO: Isso apaga TODOS os dados!
python manage.py flush
python manage.py migrate
```

## Troubleshooting

### Problema: "No module named 'django'"
**Solução**: Ative o ambiente virtual e instale as dependências
```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Problema: "ModuleNotFoundError"
**Solução**: Verifique se está no diretório correto
```bash
cd C:\Users\Revol\Documents\PLATAFORMA-RESUMO-ACADEMICO
python manage.py teste_assuntos
```

### Problema: Nenhum resultado
**Solução**: Verifique se há dados no banco
```bash
python manage.py shell -c "from questoes.models import Assunto; print(Assunto.objects.count())"
```

## Notas Importantes

1. **Privacidade**: O comando de teste não expõe informações sensíveis
2. **Performance**: O comando é rápido para bancos pequenos/médios
3. **Format**: A saída é colorida usando Django's styling system
4. **Debug**: Use este comando para verificar se os dados estão corretos no banco

## Integração com Sistema de Testes

Este comando pode ser usado em testes automatizados:

```python
from django.test import TestCase
from django.core.management import call_command
from io import StringIO
from questoes.models import Assunto

class TestAssuntos(TestCase):
    def setUp(self):
        Assunto.objects.create(nome='Teste Tema', tipo_assunto='tema')
        Assunto.objects.create(nome='Teste Concurso', tipo_assunto='concurso')
    
    def test_lista_assuntos(self):
        out = StringIO()
        call_command('teste_assuntos', stdout=out)
        output = out.getvalue()
        self.assertIn('CONCURSOS ENCONTRADOS', output)
```

