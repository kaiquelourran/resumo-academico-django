"""
Comando de gerenciamento para verificação direta da query
Replica a funcionalidade do arquivo PHP verificar_query_direta.php
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Count
from questoes.models import Assunto, Questao


class Command(BaseCommand):
    help = '🔍 Verificação Direta da Query - Debug do banco de dados'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🔍 VERIFICAÇÃO DIRETA DA QUERY'))
        self.stdout.write(self.style.WARNING('=' * 80))
        
        try:
            # 1. Query EXATA do escolher_assunto (equivalente SQL)
            self.stdout.write('\n1. Query EXATA (do escolher_assunto):')
            self.stdout.write('-' * 80)
            
            # Usar Django ORM para replicar a query SQL
            assuntos_com_questoes = Assunto.objects.annotate(
                total_questoes=Count('questoes')
            ).order_by('tipo_assunto', 'nome')
            
            self.stdout.write('SQL equivalente (ORM):')
            self.stdout.write('  Assunto.objects.annotate(total_questoes=Count("questoes"))')
            self.stdout.write('-' * 80)
            
            # Print headers
            self.stdout.write(f"{'ID':<5} {'Nome':<40} {'tipo_assunto':<20} {'Questões':<10}")
            self.stdout.write('-' * 80)
            
            for assunto in assuntos_com_questoes:
                tipo = assunto.tipo_assunto or 'NULL'
                if tipo == 'concurso':
                    self.stdout.write(
                        self.style.WARNING(
                            f"{assunto.id:<5} {assunto.nome:<40} {tipo:<20} {assunto.total_questoes:<10}"
                        )
                    )
                else:
                    self.stdout.write(f"{assunto.id:<5} {assunto.nome:<40} {tipo:<20} {assunto.total_questoes:<10}")
            
            self.stdout.write(f'\nTotal de linhas retornadas: {assuntos_com_questoes.count()}')
            
            # 2. Verificar se ID específico existe
            self.stdout.write('\n2. Verificação Direta do ID (escolha um ID):')
            self.stdout.write('-' * 80)
            
            # Tentar encontrar o primeiro assunto com questões
            primeiro_assunto = assuntos_com_questoes.first()
            if primeiro_assunto:
                self.stdout.write(f'\nVerificando ID {primeiro_assunto.id}:')
                assunto_teste = Assunto.objects.get(id=primeiro_assunto.id)
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ ID {assunto_teste.id} EXISTE na tabela assuntos')
                )
                self.stdout.write(f'Nome: {assunto_teste.nome}')
                self.stdout.write(f'Tipo: {assunto_teste.tipo_assunto}')
                self.stdout.write(f'Questões: {assunto_teste.total_questoes}')
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Nenhum assunto encontrado!')
                )
            
            # 3. Verificar TODOS os IDs da tabela assuntos
            self.stdout.write('\n3. TODOS os IDs da Tabela \'assuntos\':')
            self.stdout.write('-' * 80)
            
            todos_assuntos = Assunto.objects.all().order_by('id')
            
            self.stdout.write(f"{'ID':<5} {'Nome':<40} {'tipo_assunto':<20}")
            self.stdout.write('-' * 80)
            
            for assunto in todos_assuntos:
                tipo = assunto.tipo_assunto or 'NULL'
                if tipo == 'concurso':
                    self.stdout.write(
                        self.style.WARNING(f"{assunto.id:<5} {assunto.nome:<40} {tipo:<20}")
                    )
                else:
                    self.stdout.write(f"{assunto.id:<5} {assunto.nome:<40} {tipo:<20}")
            
            # 4. Verificar sem agregação (para comparar)
            self.stdout.write('\n4. Query SEM Agregação (para comparar):')
            self.stdout.write('-' * 80)
            
            assuntos_simples = Assunto.objects.all().order_by('tipo_assunto', 'nome')
            
            self.stdout.write(f"{'ID':<5} {'Nome':<40} {'tipo_assunto':<20}")
            self.stdout.write('-' * 80)
            
            for assunto in assuntos_simples:
                tipo = assunto.tipo_assunto or 'NULL'
                if tipo == 'concurso':
                    self.stdout.write(
                        self.style.WARNING(f"{assunto.id:<5} {assunto.nome:<40} {tipo:<20}")
                    )
                else:
                    self.stdout.write(f"{assunto.id:<5} {assunto.nome:<40} {tipo:<20}")
            
            self.stdout.write(f'\nTotal de linhas retornadas: {assuntos_simples.count()}')
            
            # 5. Verificar questões de um assunto específico
            self.stdout.write('\n5. Questões Associadas (primeiro assunto com questões):')
            self.stdout.write('-' * 80)
            
            if primeiro_assunto:
                questoes = Questao.objects.filter(id_assunto=primeiro_assunto.id)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Questões encontradas para ID {primeiro_assunto.id}: {questoes.count()}'
                    )
                )
                
                if questoes.exists():
                    self.stdout.write(f"{'ID':<10} {'Enunciado':<60} {'ID Assunto':<15}")
                    self.stdout.write('-' * 80)
                    
                    for questao in questoes[:5]:  # Mostrar primeiras 5
                        enunciado = questao.texto[:60] + "..." if len(questao.texto) > 60 else questao.texto
                        self.stdout.write(f"{questao.id:<10} {enunciado:<60} {questao.id_assunto_id:<15}")
                else:
                    self.stdout.write(
                        self.style.WARNING('⚠️ Nenhuma questão encontrada')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Nenhum assunto disponível para verificar')
                )
            
            # 6. Diagnóstico final
            self.stdout.write('\n6. 🎯 DIAGNÓSTICO FINAL:')
            self.stdout.write('-' * 80)
            
            # Contar por tipo
            temas = assuntos_com_questoes.filter(tipo_assunto='tema').count()
            concursos = assuntos_com_questoes.filter(tipo_assunto='concurso').count()
            profissionais = assuntos_com_questoes.filter(tipo_assunto='profissional').count()
            
            self.stdout.write(f'Temas: {temas}')
            self.stdout.write(f'Concursos: {concursos}')
            self.stdout.write(f'Profissionais: {profissionais}')
            
            if concursos == 0:
                self.stdout.write(
                    self.style.ERROR(
                        '\n❌ PROBLEMA: Nenhum concurso encontrado na query!'
                    )
                )
                self.stdout.write('Verifique:')
                self.stdout.write('  1. Se há assuntos com tipo_assunto="concurso"')
                self.stdout.write('  2. Se o GROUP BY está funcionando corretamente')
                self.stdout.write('  3. Se há questões associadas aos concursos')
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✅ {concursos} concurso(s) encontrado(s) corretamente na query!'
                    )
                )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro: {str(e)}')
            )

