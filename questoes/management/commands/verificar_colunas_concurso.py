"""
Comando de gerenciamento para verificar e adicionar colunas de concurso
Replica a funcionalidade do arquivo PHP verificar_colunas_concurso.php
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from questoes.models import Assunto


class Command(BaseCommand):
    help = '🔍 Verificação de Colunas de Concurso'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🔍 VERIFICAÇÃO DE COLUNAS DE CONCURSO'))
        self.stdout.write(self.style.WARNING('=' * 50))
        
        try:
            # Verificar estrutura atual da tabela assuntos
            self.stdout.write('\n1. Estrutura atual da tabela \'assuntos\':')
            self.stdout.write('-' * 80)
            
            with connection.cursor() as cursor:
                cursor.execute("DESCRIBE assuntos")
                columns = cursor.fetchall()
                
                # Print headers
                self.stdout.write(f"{'Campo':<20} {'Tipo':<20} {'Null':<10} {'Key':<10} {'Extra':<10}")
                self.stdout.write('-' * 80)
                
                colunas_existentes = []
                for col in columns:
                    campo, tipo, null, key, default, extra = col
                    self.stdout.write(f"{campo:<20} {tipo:<20} {null:<10} {key:<10} {extra or '':<10}")
                    colunas_existentes.append(campo)
            
            # Verificar se as colunas de concurso existem
            self.stdout.write('\n2. Verificação das colunas de concurso:')
            
            colunas_necessarias = [
                'concurso_ano',
                'concurso_banca',
                'concurso_orgao',
                'concurso_prova'
            ]
            
            faltam_colunas = False
            
            for coluna in colunas_necessarias:
                if coluna in colunas_existentes:
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Coluna '{coluna}' existe")
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Coluna '{coluna}' NÃO existe")
                    )
                    faltam_colunas = True
            
            # Adicionar colunas faltantes via migrations
            if faltam_colunas:
                self.stdout.write('\n3. Criando migration para adicionar colunas faltantes:')
                try:
                    # Usar o modelo Django para verificar se as colunas existem no modelo
                    from django.db import models
                    from questoes.models import Assunto
                    
                    # Verificar se as colunas existem no modelo
                    model_fields = [f.name for f in Assunto._meta.get_fields()]
                    
                    if 'concurso_ano' not in model_fields:
                        self.stdout.write(
                            self.style.WARNING(
                                '⚠️ Campos de concurso não estão no modelo Django.'
                            )
                        )
                        self.stdout.write(
                            'Execute as migrações para adicionar os campos:\n'
                            '  python manage.py makemigrations\n'
                            '  python manage.py migrate'
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS('✅ Campos estão no modelo Django')
                        )
                        self.stdout.write('Execute as migrações: python manage.py migrate')
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Erro: {str(e)}')
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS('✅ Todas as colunas de concurso já existem!')
                )
            
            # Verificar se existem assuntos de concurso
            self.stdout.write('\n4. Assuntos de concurso existentes:')
            
            try:
                concursos = Assunto.objects.filter(tipo_assunto='concurso')
                
                if not concursos.exists():
                    self.stdout.write(
                        self.style.WARNING('⚠️ Nenhum assunto de concurso encontrado!')
                    )
                    self.stdout.write('Para criar um concurso, use o Django Admin ou shell')
                else:
                    self.stdout.write(f'Encontrados {concursos.count()} concursos:')
                    self.stdout.write('-' * 100)
                    self.stdout.write(f"{'ID':<5} {'Nome':<40} {'Ano':<10} {'Banca':<20} {'Órgão':<20} {'Prova':<20}")
                    self.stdout.write('-' * 100)
                    
                    for concurso in concursos:
                        self.stdout.write(
                            f"{concurso.id:<5} "
                            f"{concurso.nome:<40} "
                            f"{concurso.concurso_ano or 'NULL':<10} "
                            f"{concurso.concurso_banca or 'NULL':<20} "
                            f"{concurso.concurso_orgao or 'NULL':<20} "
                            f"{concurso.concurso_prova or 'NULL':<20}"
                        )
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Erro ao buscar concursos: {str(e)}')
                )
            
            self.stdout.write('\n' + '=' * 50)
            self.stdout.write('\nPróximos passos:')
            self.stdout.write('1. Se faltavam colunas, execute: python manage.py migrate')
            self.stdout.write('2. Se não existem concursos, crie um via Django Admin')
            self.stdout.write('3. Depois teste adicionar uma questão de concurso')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro geral: {str(e)}')
            )

