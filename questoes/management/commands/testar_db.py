"""
Comando Django para testar conexão com o banco de dados
Uso: python manage.py testar_db
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings
import sys


class Command(BaseCommand):
    help = 'Testa a conexão com o banco de dados PostgreSQL configurado'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("TESTE DE CONEXÃO COM BANCO DE DADOS"))
        self.stdout.write("=" * 70)
        self.stdout.write("")
        
        # Mostra configuração
        db_settings = settings.DATABASES['default']
        self.stdout.write("📋 Configuração:")
        self.stdout.write(f"   Engine:   {db_settings.get('ENGINE', 'N/A')}")
        self.stdout.write(f"   Host:     {db_settings.get('HOST', 'localhost')}")
        self.stdout.write(f"   Porta:    {db_settings.get('PORT', '5432')}")
        self.stdout.write(f"   Banco:    {db_settings.get('NAME', 'N/A')}")
        self.stdout.write(f"   Usuário:  {db_settings.get('USER', 'N/A')}")
        self.stdout.write(f"   Senha:    {'*' * len(db_settings.get('PASSWORD', '')) if db_settings.get('PASSWORD') else '(vazia)'}")
        self.stdout.write("")
        
        try:
            self.stdout.write("🔄 Tentando conectar...")
            
            # Tenta conectar
            with connection.cursor() as cursor:
                # Testa query simples
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                
                self.stdout.write(self.style.SUCCESS("✅ CONEXÃO BEM-SUCEDIDA!"))
                self.stdout.write("")
                self.stdout.write(f"📊 Versão do PostgreSQL:")
                self.stdout.write(f"   {version[0][:80]}...")
                self.stdout.write("")
                
                # Lista bancos de dados
                cursor.execute("""
                    SELECT datname 
                    FROM pg_database 
                    WHERE datistemplate = false 
                    ORDER BY datname;
                """)
                databases = cursor.fetchall()
                self.stdout.write(f"📁 Bancos de dados disponíveis ({len(databases)}):")
                for db in databases:
                    marker = self.style.SUCCESS(" ← (usando)") if db[0] == db_settings.get('NAME') else ""
                    self.stdout.write(f"   - {db[0]}{marker}")
                self.stdout.write("")
                
                # Lista tabelas do banco atual
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                if tables:
                    self.stdout.write(f"📋 Tabelas no banco '{db_settings.get('NAME')}' ({len(tables)}):")
                    for table in tables[:15]:  # Mostra apenas as 15 primeiras
                        self.stdout.write(f"   - {table[0]}")
                    if len(tables) > 15:
                        self.stdout.write(f"   ... e mais {len(tables) - 15} tabelas")
                else:
                    self.stdout.write(f"📋 Nenhuma tabela encontrada no banco '{db_settings.get('NAME')}'")
                self.stdout.write("")
            
            self.stdout.write("=" * 70)
            self.stdout.write(self.style.SUCCESS("✅ TESTE CONCLUÍDO COM SUCESSO!"))
            self.stdout.write("=" * 70)
            
        except Exception as e:
            self.stdout.write("=" * 70)
            self.stdout.write(self.style.ERROR("❌ ERRO DE CONEXÃO"))
            self.stdout.write("=" * 70)
            self.stdout.write("")
            self.stdout.write(self.style.ERROR(f"   {str(e)}"))
            self.stdout.write("")
            
            error_msg = str(e).lower()
            
            if "password authentication failed" in error_msg:
                self.stdout.write(self.style.WARNING("🔍 DIAGNÓSTICO:"))
                self.stdout.write("   A senha está INCORRETA ou o usuário não existe.")
                self.stdout.write("")
                self.stdout.write(self.style.WARNING("💡 SOLUÇÕES:"))
                self.stdout.write("   1. Verifique a senha no arquivo .env")
                self.stdout.write("   2. Verifique se o usuário existe no servidor PostgreSQL")
                self.stdout.write(f"   3. Acesse o pgAdmin: http://{db_settings.get('HOST', 'localhost')}:5050/browser/")
                
            elif "could not connect" in error_msg or "connection refused" in error_msg:
                self.stdout.write(self.style.WARNING("🔍 DIAGNÓSTICO:"))
                self.stdout.write("   Não foi possível conectar ao servidor.")
                self.stdout.write("")
                self.stdout.write(self.style.WARNING("💡 SOLUÇÕES:"))
                self.stdout.write("   1. Verifique se o PostgreSQL está rodando")
                self.stdout.write("   2. Verifique se o IP/Host está correto")
                self.stdout.write("   3. Verifique se a porta está correta")
                self.stdout.write("   4. Verifique se o firewall permite conexões")
            
            self.stdout.write("")
            self.stdout.write("=" * 70)
            sys.exit(1)

