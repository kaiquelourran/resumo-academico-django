#!/usr/bin/env python
"""
Script para testar conexão com PostgreSQL
Testa as credenciais configuradas no arquivo .env
"""
import os
import sys
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

try:
    import psycopg2
    from psycopg2 import OperationalError
except ImportError:
    print("❌ ERRO: psycopg2 não está instalado!")
    print("   Instale com: pip install psycopg2-binary")
    sys.exit(1)

# Obtém credenciais do .env
db_config = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'postgres'),
    'user': os.getenv('POSTGRES_USER', 'admin'),
    'password': os.getenv('POSTGRES_PASSWORD', ''),
}

def testar_conexao():
    """Testa a conexão com o banco de dados PostgreSQL"""
    
    print("=" * 70)
    print("TESTE DE CONEXÃO COM POSTGRESQL")
    print("=" * 70)
    print()
    print("📋 Configuração:")
    print(f"   Host:     {db_config['host']}")
    print(f"   Porta:    {db_config['port']}")
    print(f"   Banco:    {db_config['database']}")
    print(f"   Usuário:  {db_config['user']}")
    print(f"   Senha:    {'*' * len(db_config['password']) if db_config['password'] else '(vazia)'}")
    print()
    
    # Validações básicas
    if not db_config['password']:
        print("⚠️  AVISO: Senha não configurada no .env!")
        print()
    
    try:
        print("🔄 Tentando conectar...")
        conn = psycopg2.connect(**db_config)
        print("✅ CONEXÃO BEM-SUCEDIDA!")
        print()
        
        # Testa uma query simples
        cursor = conn.cursor()
        
        # Versão do PostgreSQL
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📊 Versão do PostgreSQL:")
        print(f"   {version[0][:80]}...")
        print()
        
        # Lista bancos de dados
        cursor.execute("""
            SELECT datname 
            FROM pg_database 
            WHERE datistemplate = false 
            ORDER BY datname;
        """)
        databases = cursor.fetchall()
        print(f"📁 Bancos de dados disponíveis ({len(databases)}):")
        for db in databases:
            marker = " ← (usando)" if db[0] == db_config['database'] else ""
            print(f"   - {db[0]}{marker}")
        print()
        
        # Lista tabelas do banco atual
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        if tables:
            print(f"📋 Tabelas no banco '{db_config['database']}' ({len(tables)}):")
            for table in tables[:10]:  # Mostra apenas as 10 primeiras
                print(f"   - {table[0]}")
            if len(tables) > 10:
                print(f"   ... e mais {len(tables) - 10} tabelas")
        else:
            print(f"📋 Nenhuma tabela encontrada no banco '{db_config['database']}'")
        print()
        
        cursor.close()
        conn.close()
        
        print("=" * 70)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        return True
        
    except OperationalError as e:
        print("=" * 70)
        print("❌ ERRO DE CONEXÃO")
        print("=" * 70)
        print()
        error_msg = str(e)
        print(f"   {error_msg}")
        print()
        
        # Análise do erro
        if "password authentication failed" in error_msg.lower():
            print("🔍 DIAGNÓSTICO:")
            print("   A senha está INCORRETA ou o usuário não existe.")
            print()
            print("💡 SOLUÇÕES:")
            print("   1. Verifique a senha no arquivo .env")
            print("   2. Verifique se o usuário existe no servidor PostgreSQL")
            print("   3. Acesse o pgAdmin para confirmar as credenciais:")
            print(f"      http://{db_config['host']}:5050/browser/")
            print("   4. Verifique se há espaços ou caracteres especiais na senha")
            
        elif "could not connect" in error_msg.lower() or "connection refused" in error_msg.lower():
            print("🔍 DIAGNÓSTICO:")
            print("   Não foi possível conectar ao servidor.")
            print()
            print("💡 SOLUÇÕES:")
            print("   1. Verifique se o PostgreSQL está rodando")
            print("   2. Verifique se o IP/Host está correto")
            print("   3. Verifique se a porta está correta (5432)")
            print("   4. Verifique se o firewall permite conexões")
            print("   5. Verifique se o servidor permite conexões remotas")
            
        elif "database" in error_msg.lower() and "does not exist" in error_msg.lower():
            print("🔍 DIAGNÓSTICO:")
            print("   O banco de dados não existe.")
            print()
            print("💡 SOLUÇÕES:")
            print(f"   1. Crie o banco '{db_config['database']}' no PostgreSQL")
            print("   2. Ou altere POSTGRES_DB no .env para um banco existente")
            
        else:
            print("🔍 Verifique a mensagem de erro acima para mais detalhes.")
        
        print()
        print("=" * 70)
        return False
        
    except Exception as e:
        print("=" * 70)
        print("❌ ERRO INESPERADO")
        print("=" * 70)
        print()
        print(f"   {type(e).__name__}: {str(e)}")
        print()
        print("=" * 70)
        return False

if __name__ == "__main__":
    sucesso = testar_conexao()
    sys.exit(0 if sucesso else 1)

