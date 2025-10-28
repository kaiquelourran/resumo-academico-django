from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questoes.models import Assunto, Questao, Alternativa, RespostaUsuario
import mysql.connector
from mysql.connector import Error

class Command(BaseCommand):
    help = 'Importa dados do MySQL (XAMPP) para o PostgreSQL (Django)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--host',
            type=str,
            default='host.docker.internal',
            help='Host do MySQL (use host.docker.internal para XAMPP no Windows)'
        )
        parser.add_argument(
            '--database',
            type=str,
            default='resumo_quiz',
            help='Nome do banco de dados MySQL'
        )
        parser.add_argument(
            '--user',
            type=str,
            default='root',
            help='Usuário do MySQL'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='',
            help='Senha do MySQL'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando importação do MySQL...'))
        
        try:
            # Conectar ao MySQL
            connection = mysql.connector.connect(
                host=options['host'],
                database=options['database'],
                user=options['user'],
                password=options['password']
            )
            
            if connection.is_connected():
                self.stdout.write(self.style.SUCCESS('✓ Conectado ao MySQL'))
                cursor = connection.cursor(dictionary=True)
                
                # 1. Importar Assuntos
                self.stdout.write('Importando assuntos...')
                cursor.execute("SELECT * FROM assuntos")
                assuntos = cursor.fetchall()
                
                assunto_map = {}
                for assunto in assuntos:
                    tipo = 'tema'
                    if assunto.get('tipo_assunto'):
                        tipo_lower = assunto['tipo_assunto'].lower()
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
                        self.stdout.write(f"  + {obj.nome}")
                
                self.stdout.write(self.style.SUCCESS(f'✓ {len(assuntos)} assuntos importados'))
                
                # 2. Importar Questões
                self.stdout.write('Importando questões...')
                cursor.execute("SELECT * FROM questoes")
                questoes = cursor.fetchall()
                
                questao_map = {}
                for questao in questoes:
                    try:
                        assunto = assunto_map.get(questao['id_assunto'])
                        if not assunto:
                            self.stdout.write(self.style.WARNING(f"  Pulando questão {questao['id_questao']} - assunto não encontrado"))
                            continue
                        
                        obj, created = Questao.objects.get_or_create(
                            id=questao['id_questao'],
                            defaults={
                                'texto': questao['texto'],
                                'id_assunto': assunto,
                                'explicacao': questao.get('explicacao', '')
                            }
                        )
                        questao_map[questao['id_questao']] = obj
                        if created and questao['id_questao'] % 10 == 0:
                            self.stdout.write(f"  + {questao['id_questao']} questões...")
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"  Erro na questão {questao['id_questao']}: {str(e)}"))
                
                self.stdout.write(self.style.SUCCESS(f'✓ {len(questoes)} questões importadas'))
                
                # 3. Importar Alternativas
                self.stdout.write('Importando alternativas...')
                cursor.execute("SELECT * FROM alternativas ORDER BY id_questao, id_alternativa")
                alternativas = cursor.fetchall()
                
                for idx, alternativa in enumerate(alternativas):
                    try:
                        questao = questao_map.get(alternativa['id_questao'])
                        if not questao:
                            continue
                        
                        Alternativa.objects.get_or_create(
                            id=alternativa['id_alternativa'],
                            defaults={
                                'id_questao': questao,
                                'texto': alternativa['texto'],
                                'eh_correta': bool(alternativa['eh_correta']),
                                'ordem': idx % 4 + 1
                            }
                        )
                        if (idx + 1) % 100 == 0:
                            self.stdout.write(f"  + {idx + 1} alternativas...")
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"  Erro na alternativa {alternativa['id_alternativa']}: {str(e)}"))
                
                self.stdout.write(self.style.SUCCESS(f'✓ {len(alternativas)} alternativas importadas'))
                
                # 4. Importar Usuários
                self.stdout.write('Importando usuários...')
                cursor.execute("SELECT * FROM usuarios")
                usuarios = cursor.fetchall()
                
                usuario_map = {}
                for usuario in usuarios:
                    try:
                        username = usuario['email'].split('@')[0][:30]  # Limitar a 30 caracteres
                        
                        # Verificar se já existe
                        if User.objects.filter(email=usuario['email']).exists():
                            user = User.objects.get(email=usuario['email'])
                        else:
                            user = User.objects.create_user(
                                username=username,
                                email=usuario['email'],
                                first_name=usuario.get('nome', '')[:30],
                                password='!impossivel_login'  # Hash temporário
                            )
                            # Definir a senha com hash do PHP
                            user.password = usuario['senha']
                            user.save()
                        
                        usuario_map[usuario.get('id_usuario') or usuario.get('id')] = user
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"  Erro no usuário {usuario.get('email')}: {str(e)}"))
                
                self.stdout.write(self.style.SUCCESS(f'✓ {len(usuarios)} usuários importados'))
                
                # Fechar conexão
                cursor.close()
                connection.close()
                
                self.stdout.write(self.style.SUCCESS('\n✅ Importação concluída com sucesso!'))
                self.stdout.write(self.style.SUCCESS(f'   Assuntos: {Assunto.objects.count()}'))
                self.stdout.write(self.style.SUCCESS(f'   Questões: {Questao.objects.count()}'))
                self.stdout.write(self.style.SUCCESS(f'   Alternativas: {Alternativa.objects.count()}'))
                self.stdout.write(self.style.SUCCESS(f'   Usuários: {User.objects.count()}'))
                
        except Error as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao conectar ao MySQL: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro: {e}'))


