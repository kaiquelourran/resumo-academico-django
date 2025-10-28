"""
Comando de gerenciamento para testar a estrutura do banco de dados
Replica a funcionalidade do arquivo PHP teste_simples.php
"""

from django.core.management.base import BaseCommand
from questoes.models import Assunto


class Command(BaseCommand):
    help = '🧪 TESTE SIMPLES - FORÇA BRUTA: Lista todos os assuntos do banco'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🧪 TESTE SIMPLES - FORÇA BRUTA'))
        self.stdout.write(self.style.WARNING('=' * 50))
        
        try:
            # Query SIMPLES sem GROUP BY
            assuntos = Assunto.objects.all().order_by('tipo_assunto', 'nome')
            
            self.stdout.write('\n📊 TODOS OS ASSUNTOS:')
            self.stdout.write('-' * 80)
            
            temas = 0
            concursos = 0
            profissionais = 0
            
            # Print headers
            self.stdout.write(f"{'ID':<5} {'Nome':<40} {'Tipo':<15}")
            self.stdout.write('-' * 80)
            
            for assunto in assuntos:
                if assunto.tipo_assunto == 'concurso':
                    self.stdout.write(
                        self.style.WARNING(
                            f"{assunto.id:<5} {assunto.nome:<40} {assunto.tipo_assunto:<15}"
                        )
                    )
                    concursos += 1
                elif assunto.tipo_assunto == 'profissional':
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{assunto.id:<5} {assunto.nome:<40} {assunto.tipo_assunto:<15}"
                        )
                    )
                    profissionais += 1
                else:
                    self.stdout.write(f"{assunto.id:<5} {assunto.nome:<40} {assunto.tipo_assunto:<15}")
                    temas += 1
            
            self.stdout.write('\n📈 CONTAGEM:')
            self.stdout.write(f"Temas: {temas}")
            self.stdout.write(f"Concursos: {concursos}")
            self.stdout.write(f"Profissionais: {profissionais}")
            
            if concursos > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        '\n✅ CONCURSOS ENCONTRADOS! O problema NÃO é no banco de dados.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        '\n❌ NENHUM CONCURSO ENCONTRADO! O problema É no banco de dados.'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro: {str(e)}')
            )

