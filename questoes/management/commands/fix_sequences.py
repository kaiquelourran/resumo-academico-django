"""
Comando Django para corrigir sequências do PostgreSQL que estão dessincronizadas.
Execute: python manage.py fix_sequences
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Corrige sequências do PostgreSQL que estão dessincronizadas'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Lista de tabelas e seus campos ID
            tables = [
                ('questoes_comentarioquestao', 'id'),
                ('questoes_curtidacomentario', 'id'),
                ('questoes_denunciacomentario', 'id'),
                ('questoes_questao', 'id'),
                ('questoes_alternativa', 'id'),
                ('questoes_respostausuario', 'id'),
                ('questoes_assunto', 'id'),
                ('questoes_relatoriobug', 'id'),
            ]
            
            self.stdout.write(self.style.SUCCESS('Corrigindo sequencias do PostgreSQL...\n'))
            
            for table_name, id_field in tables:
                try:
                    # Pega o máximo ID atual na tabela
                    cursor.execute(f"SELECT MAX({id_field}) FROM {table_name};")
                    max_id = cursor.fetchone()[0]
                    
                    if max_id is None:
                        max_id = 0
                        self.stdout.write(f"   {table_name}: Nenhum registro encontrado, definindo sequencia para 1")
                    else:
                        self.stdout.write(f"   {table_name}: ID maximo = {max_id}, ajustando sequencia para {max_id + 1}")
                    
                    # Ajusta a sequência para o próximo valor disponível
                    sequence_name = f"{table_name}_{id_field}_seq"
                    cursor.execute(f"SELECT setval('{sequence_name}', COALESCE((SELECT MAX({id_field}) FROM {table_name}), 1), true);")
                    
                    self.stdout.write(self.style.SUCCESS(f"   OK - {table_name}: Sequencia corrigida!\n"))
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"   ERRO - {table_name}: {str(e)}\n"))
            
            self.stdout.write(self.style.SUCCESS('\nSequencias corrigidas com sucesso!'))

