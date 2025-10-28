from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questoes.models import Assunto, Questao, Alternativa
import re

class Command(BaseCommand):
    help = 'Importa dados do arquivo SQL do MySQL para o Django'

    def add_arguments(self, parser):
        parser.add_argument(
            'sql_file',
            type=str,
            help='Caminho para o arquivo SQL (resumo_quiz_limpo.sql)'
        )

    def handle(self, *args, **options):
        sql_file = options['sql_file']
        
        self.stdout.write(self.style.SUCCESS(f'Lendo arquivo: {sql_file}'))
        
        try:
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # 1. Extrair e importar Assuntos
            self.stdout.write('Importando assuntos...')
            assunto_pattern = r"INSERT INTO `assuntos`.*?VALUES\s+(.*?);"
            assunto_matches = re.findall(assunto_pattern, sql_content, re.DOTALL)
            
            assunto_map = {}
            for match in assunto_matches:
                # Extrair valores individuais
                rows = re.findall(r"\(([^)]+)\)", match)
                for row in rows:
                    values = [v.strip().strip("'\"") for v in row.split(',')]
                    if len(values) >= 2:
                        id_assunto = int(values[0])
                        nome = values[1]
                        tipo_assunto = values[2] if len(values) > 2 else 'tema'
                        
                        # Normalizar tipo
                        tipo_lower = tipo_assunto.lower()
                        if 'concurso' in tipo_lower:
                            tipo = 'concurso'
                        elif 'profissional' in tipo_lower:
                            tipo = 'profissional'
                        else:
                            tipo = 'tema'
                        
                        obj, created = Assunto.objects.get_or_create(
                            id=id_assunto,
                            defaults={'nome': nome, 'tipo_assunto': tipo}
                        )
                        assunto_map[id_assunto] = obj
                        if created:
                            self.stdout.write(f"  + {nome}")
            
            self.stdout.write(self.style.SUCCESS(f'✓ {len(assunto_map)} assuntos importados'))
            
            # 2. Extrair e importar Questões
            self.stdout.write('Importando questões...')
            questao_pattern = r"INSERT INTO `questoes`.*?VALUES\s+(.*?);"
            questao_matches = re.findall(questao_pattern, sql_content, re.DOTALL)
            
            questao_map = {}
            questao_count = 0
            for match in questao_matches:
                rows = re.findall(r"\(([^)]+)\)", match)
                for row in rows:
                    # Parse mais robusto para questões com vírgulas no texto
                    parts = row.split("', '")
                    if len(parts) >= 3:
                        id_questao = int(parts[0].strip("'\""))
                        texto = parts[1] if len(parts) > 1 else ''
                        id_assunto = int(parts[2].strip("'\"")) if len(parts) > 2 else None
                        explicacao = parts[3].strip("'\"") if len(parts) > 3 else ''
                        
                        if id_assunto and id_assunto in assunto_map:
                            obj, created = Questao.objects.get_or_create(
                                id=id_questao,
                                defaults={
                                    'texto': texto,
                                    'id_assunto': assunto_map[id_assunto],
                                    'explicacao': explicacao
                                }
                            )
                            questao_map[id_questao] = obj
                            questao_count += 1
                            if questao_count % 10 == 0:
                                self.stdout.write(f"  + {questao_count} questões...")
            
            self.stdout.write(self.style.SUCCESS(f'✓ {questao_count} questões importadas'))
            
            # 3. Extrair e importar Alternativas
            self.stdout.write('Importando alternativas...')
            alternativa_pattern = r"INSERT INTO `alternativas`.*?VALUES\s+(.*?);"
            alternativa_matches = re.findall(alternativa_pattern, sql_content, re.DOTALL)
            
            alternativa_count = 0
            for match in alternativa_matches:
                rows = re.findall(r"\(([^)]+)\)", match)
                for idx, row in enumerate(rows):
                    parts = row.split("', '")
                    if len(parts) >= 3:
                        id_alternativa = int(parts[0].strip("'\""))
                        id_questao = int(parts[1].strip("'\""))
                        texto = parts[2] if len(parts) > 2 else ''
                        eh_correta = parts[3].strip("'\"") == '1' if len(parts) > 3 else False
                        
                        if id_questao in questao_map:
                            Alternativa.objects.get_or_create(
                                id=id_alternativa,
                                defaults={
                                    'id_questao': questao_map[id_questao],
                                    'texto': texto,
                                    'eh_correta': eh_correta,
                                    'ordem': (alternativa_count % 4) + 1
                                }
                            )
                            alternativa_count += 1
                            if alternativa_count % 100 == 0:
                                self.stdout.write(f"  + {alternativa_count} alternativas...")
            
            self.stdout.write(self.style.SUCCESS(f'✓ {alternativa_count} alternativas importadas'))
            
            self.stdout.write(self.style.SUCCESS('\n✅ Importação concluída!'))
            self.stdout.write(self.style.SUCCESS(f'   Assuntos: {Assunto.objects.count()}'))
            self.stdout.write(self.style.SUCCESS(f'   Questões: {Questao.objects.count()}'))
            self.stdout.write(self.style.SUCCESS(f'   Alternativas: {Alternativa.objects.count()}'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'❌ Arquivo não encontrado: {sql_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro: {e}'))
            import traceback
            traceback.print_exc()


