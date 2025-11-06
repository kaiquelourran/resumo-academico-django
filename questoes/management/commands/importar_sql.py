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
            # Buscar INSERT statements completos (incluindo quebras de linha)
            questao_inserts = re.findall(r"INSERT INTO `questoes`[^;]+;", sql_content, re.DOTALL)
            
            questao_map = {}
            questao_count = 0
            questao_atualizadas = 0
            questao_erros = 0
            
            for insert in questao_inserts:
                try:
                    # Extrair id_questao (primeiro campo)
                    id_match = re.search(r"VALUES\s*\(\s*'(\d+)'", insert)
                    if not id_match:
                        questao_erros += 1
                        continue
                    
                    id_questao = int(id_match.group(1))
                    
                    # Extrair id_assunto (segundo campo)
                    assunto_match = re.search(r"VALUES\s*\(\s*'\d+',\s*'(\d+)'", insert)
                    if not assunto_match:
                        questao_erros += 1
                        continue
                    
                    id_assunto = int(assunto_match.group(1))
                    if id_assunto not in assunto_map:
                        questao_erros += 1
                        continue
                    
                    # Extrair enunciado (terceiro campo) - pode ter quebras de linha
                    # Padrão: 'id', 'assunto', 'enunciado...', 'explicacao', ...
                    # Melhorar regex para capturar corretamente o enunciado com quebras de linha
                    # Procura por: VALUES ('id', 'assunto', 'enunciado...', 'explicacao'
                    enunciado_match = re.search(
                        r"VALUES\s*\(\s*'\d+',\s*'\d+',\s*'((?:[^']|'')+?)',\s*'",
                        insert, 
                        re.DOTALL
                    )
                    
                    enunciado = ''
                    if enunciado_match:
                        enunciado_raw = enunciado_match.group(1)
                        # Limpar o enunciado (remover escapes de aspas simples)
                        enunciado = enunciado_raw.replace("''", "'")
                        # Normalizar quebras de linha e espaços extras
                        # Preservar quebras de linha significativas, mas normalizar múltiplos espaços
                        enunciado = re.sub(r'\s+', ' ', enunciado)  # Substituir múltiplos espaços/line breaks por um espaço
                        enunciado = enunciado.strip()
                    
                    # Validação: garantir que o enunciado não seja uma string vazia
                    if not enunciado or len(enunciado) == 0:
                        # Log de depuração para questões sem enunciado
                        self.stdout.write(self.style.WARNING(
                            f"  ⚠ Questão ID {id_questao}: Enunciado vazio ou None no SQL"
                        ))
                        enunciado = ''  # Garantir que seja string vazia, não None
                    
                    # Log de depuração temporário (mostra início do texto lido)
                    if enunciado:
                        texto_preview = enunciado[:50] + '...' if len(enunciado) > 50 else enunciado
                        self.stdout.write(self.style.SUCCESS(
                            f"  DEBUG: Questão ID {id_questao} lida. Texto ({len(enunciado)} chars) começa com: '{texto_preview}'"
                        ))
                    
                    # Extrair explicacao (quarto campo)
                    explicacao_match = re.search(
                        r"VALUES\s*\(\s*'\d+',\s*'\d+',\s*'[^']+',\s*'([^']*)'",
                        insert,
                        re.DOTALL
                    )
                    explicacao = explicacao_match.group(1) if explicacao_match else ''
                    
                    # Mapeamento crítico: Campo 'enunciado' do SQL → Campo 'texto' do Django
                    # No Django, o campo é 'texto', mas no SQL é 'enunciado'
                    
                    # Buscar ou criar a questão
                    obj, created = Questao.objects.get_or_create(
                        id=id_questao,
                        defaults={
                            'texto': enunciado,  # Campo 'enunciado' do SQL vai para 'texto' no Django
                            'id_assunto': assunto_map[id_assunto],
                            'explicacao': explicacao if explicacao else ''
                        }
                    )
                    
                    # AÇÃO CRÍTICA: Se a questão já existe, SEMPRE atualizar o campo texto
                    # se o enunciado do SQL tiver conteúdo válido
                    if not created:
                        # Sempre atualizar se houver enunciado válido no SQL
                        if enunciado and len(enunciado) > 0:
                            # Atualizar o campo texto explicitamente
                            obj.texto = enunciado  # Mapeamento direto: enunciado (SQL) → texto (Django)
                            obj.id_assunto = assunto_map[id_assunto]
                            if explicacao:
                                obj.explicacao = explicacao
                            obj.save()
                            questao_atualizadas += 1
                            self.stdout.write(self.style.SUCCESS(
                                f"  ✓ Questão ID {id_questao} ATUALIZADA: texto preenchido ({len(enunciado)} chars)"
                            ))
                        elif not obj.texto or len(obj.texto) == 0:
                            # Log de aviso se a questão existente não tem texto e o SQL também não tem
                            self.stdout.write(self.style.WARNING(
                                f"  ⚠ Questão ID {id_questao}: Sem texto no banco e no SQL"
                            ))
                    else:
                        # Questão criada com sucesso
                        if enunciado:
                            self.stdout.write(self.style.SUCCESS(
                                f"  ✓ Questão ID {id_questao} CRIADA: texto preenchido ({len(enunciado)} chars)"
                            ))
                    
                    questao_map[id_questao] = obj
                    questao_count += 1
                    
                    if questao_count % 10 == 0:
                        self.stdout.write(f"  → {questao_count} questões processadas...")
                
                except Exception as e:
                    questao_erros += 1
                    self.stdout.write(self.style.ERROR(
                        f"  ✗ Erro ao processar questão: {str(e)}"
                    ))
                    import traceback
                    self.stdout.write(traceback.format_exc())
            
            self.stdout.write(self.style.SUCCESS(f'✓ {questao_count} questões importadas'))
            if questao_atualizadas > 0:
                self.stdout.write(self.style.SUCCESS(f'✓ {questao_atualizadas} questões atualizadas'))
            if questao_erros > 0:
                self.stdout.write(self.style.WARNING(f'⚠ {questao_erros} questões com erro'))
            
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


