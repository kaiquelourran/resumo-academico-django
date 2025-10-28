from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questoes.models import Assunto, Questao, Alternativa
import json

class Command(BaseCommand):
    help = 'Importa dados do arquivo JSON exportado do PHP para o Django'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='Caminho para o arquivo JSON exportado'
        )

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        self.stdout.write(self.style.SUCCESS(f'📂 Lendo arquivo: {json_file}'))
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 1. Importar Assuntos
            self.stdout.write('\n📖 Importando assuntos...')
            assunto_map = {}
            
            for assunto in data.get('assuntos', []):
                # Normalizar tipo
                tipo = 'tema'
                tipo_assunto_raw = assunto.get('tipo_assunto', '')
                if tipo_assunto_raw:
                    tipo_lower = tipo_assunto_raw.lower()
                    if 'concurso' in tipo_lower:
                        tipo = 'concurso'
                    elif 'profissional' in tipo_lower:
                        tipo = 'profissional'
                
                obj, created = Assunto.objects.get_or_create(
                    id=assunto['id_assunto'],
                    defaults={
                        'nome': assunto['nome'],
                        'tipo_assunto': tipo
                    }
                )
                assunto_map[assunto['id_assunto']] = obj
                
                if created:
                    self.stdout.write(f"  ✓ {obj.nome}")
            
            self.stdout.write(self.style.SUCCESS(f'✅ {len(data.get("assuntos", []))} assuntos importados'))
            
            # 2. Importar Questões
            self.stdout.write('\n❓ Importando questões...')
            questao_map = {}
            questao_count = 0
            
            for questao in data.get('questoes', []):
                try:
                    assunto_id = questao['id_assunto']
                    
                    if assunto_id not in assunto_map:
                        self.stdout.write(self.style.WARNING(
                            f"  ⚠ Questão {questao['id_questao']} - assunto {assunto_id} não encontrado"
                        ))
                        continue
                    
                    obj, created = Questao.objects.get_or_create(
                        id=questao['id_questao'],
                        defaults={
                            'texto': questao['texto'],
                            'id_assunto': assunto_map[assunto_id],
                            'explicacao': questao.get('explicacao', '') or ''
                        }
                    )
                    questao_map[questao['id_questao']] = obj
                    questao_count += 1
                    
                    if questao_count % 20 == 0:
                        self.stdout.write(f"  → {questao_count} questões processadas...")
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"  ✗ Erro na questão {questao.get('id_questao')}: {str(e)}"
                    ))
            
            self.stdout.write(self.style.SUCCESS(f'✅ {questao_count} questões importadas'))
            
            # 3. Importar Alternativas
            self.stdout.write('\n📝 Importando alternativas...')
            alternativa_count = 0
            ordem_questao = {}  # Rastrear ordem por questão
            
            for alternativa in data.get('alternativas', []):
                try:
                    questao_id = alternativa['id_questao']
                    
                    if questao_id not in questao_map:
                        continue
                    
                    # Calcular ordem
                    if questao_id not in ordem_questao:
                        ordem_questao[questao_id] = 1
                    else:
                        ordem_questao[questao_id] += 1
                    
                    obj, created = Alternativa.objects.get_or_create(
                        id=alternativa['id_alternativa'],
                        defaults={
                            'id_questao': questao_map[questao_id],
                            'texto': alternativa['texto'],
                            'eh_correta': bool(int(alternativa.get('eh_correta', 0))),
                            'ordem': ordem_questao[questao_id]
                        }
                    )
                    alternativa_count += 1
                    
                    if alternativa_count % 50 == 0:
                        self.stdout.write(f"  → {alternativa_count} alternativas processadas...")
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"  ✗ Erro na alternativa {alternativa.get('id_alternativa')}: {str(e)}"
                    ))
            
            self.stdout.write(self.style.SUCCESS(f'✅ {alternativa_count} alternativas importadas'))
            
            # 4. Importar Usuários
            self.stdout.write('\n👥 Importando usuários...')
            usuario_count = 0
            
            for usuario in data.get('usuarios', []):
                try:
                    email = usuario.get('email', '')
                    if not email:
                        continue
                    
                    # Criar username a partir do email
                    username = email.split('@')[0][:30]
                    
                    # Verificar se já existe
                    if User.objects.filter(email=email).exists():
                        self.stdout.write(f"  → Usuário {email} já existe, pulando...")
                        continue
                    
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        first_name=usuario.get('nome', '')[:30],
                        password=f'temp_{username}_123'  # Senha temporária
                    )
                    
                    # Definir como staff/admin se for tipo admin
                    if usuario.get('tipo', '').lower() == 'admin':
                        user.is_staff = True
                        user.is_superuser = True
                        user.save()
                    
                    usuario_count += 1
                    self.stdout.write(f"  ✓ {email}")
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"  ✗ Erro no usuário {usuario.get('email')}: {str(e)}"
                    ))
            
            self.stdout.write(self.style.SUCCESS(f'✅ {usuario_count} usuários importados'))
            
            # Resumo final
            self.stdout.write('\n' + '='*60)
            self.stdout.write(self.style.SUCCESS('🎉 IMPORTAÇÃO CONCLUÍDA COM SUCESSO!'))
            self.stdout.write('='*60)
            self.stdout.write(f'📊 Estatísticas finais:')
            self.stdout.write(f'   • Assuntos: {Assunto.objects.count()}')
            self.stdout.write(f'   • Questões: {Questao.objects.count()}')
            self.stdout.write(f'   • Alternativas: {Alternativa.objects.count()}')
            self.stdout.write(f'   • Usuários: {User.objects.count()}')
            self.stdout.write('='*60)
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'❌ Arquivo não encontrado: {json_file}'))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao decodificar JSON: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro: {e}'))
            import traceback
            traceback.print_exc()


