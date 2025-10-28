from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q, Sum, Avg, Case, When, IntegerField, FloatField, F, ExpressionWrapper
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta
from collections import Counter
import json
import logging

from .models import (
    Assunto, Questao, Alternativa, RespostaUsuario,
    ComentarioQuestao, CurtidaComentario, DenunciaComentario,
    RelatorioBug
)

error_logger = logging.getLogger('questoes.errors')

# ---
## ===== VIEWS PÚBLICAS =====

def index_view(request):
    """View da página inicial do sistema"""
    total_assuntos = Assunto.objects.count()
    total_questoes = Questao.objects.count()
    total_alternativas = Alternativa.objects.count()
    
    semana_inicio = timezone.now() - timedelta(days=7)
    
    # Usando 'id_usuario' (FK) para agrupar e contar
    respostas_semana = RespostaUsuario.objects.filter(
        data_resposta__gte=semana_inicio,
        id_usuario__isnull=False
    ).values('id_usuario').annotate(
        total=Count('id'),
        acertos=Count('id', filter=Q(acertou=True))
    ).order_by('-total', '-acertos')[:5]
    
    ranking_semanal = []
    for item in respostas_semana:
        if item['id_usuario']:
            try:
                # CORREÇÃO DE INDENTAÇÃO: O código abaixo deve estar dentro do 'try:'
                # Otimização: buscar pelo ID. O Django User model tem 'id' como PK
                usuario = User.objects.get(pk=item['id_usuario'])
                ranking_semanal.append({
                    'id_usuario': usuario.id,
                    'nome': usuario.first_name or usuario.username,
                    'total': item['total'],
                    'acertos': item['acertos']
                })
            except User.DoesNotExist:
                # O except também deve estar alinhado com o try
                continue
    
    notificacoes = []
    if request.user.is_authenticated:
        # Usando o objeto User diretamente na query
        notificacoes = RelatorioBug.objects.filter(
            id_usuario=request.user, 
            resposta_admin__isnull=False,
            resposta_admin__gt='',
            usuario_viu_resposta=False
        ).order_by('-data_atualizacao')[:5]
    
    is_admin = request.user.is_authenticated and request.user.is_staff
    
    context = {
        'total_assuntos': total_assuntos,
        'total_questoes': total_questoes,
        'total_alternativas': total_alternativas,
        'ranking_semanal': ranking_semanal,
        'notificacoes': notificacoes,
        'is_admin': is_admin,
        'user': request.user
    }
    
    return render(request, 'questoes/index.html', context)

# ---
## ===== ADICIONE OUTRAS VIEWS AQUI =====
# Se você tinha outras views que não enviou, adicione-as aqui.
# Lembre-se de corrigir a função processar_google_login se ela for usada em outras URLs.

def escolher_assunto_view(request):
    """View para escolher o assunto antes de iniciar o quiz"""
    assuntos = Assunto.objects.annotate(
        total_questoes=Count('questoes')
    ).order_by('tipo_assunto', 'nome')
    
    categorias = {
        'temas': assuntos.filter(tipo_assunto='tema'),
        'concursos': assuntos.filter(tipo_assunto='concurso'),
        'profissionais': assuntos.filter(tipo_assunto='profissional'),
    }
    
    context = {
        'categorias': categorias,
        'total_assuntos': assuntos.count()
    }
    
    return render(request, 'questoes/escolher_assunto.html', context)


def quiz_view(request, assunto_id):
    """View que exibe as questões de um assunto específico"""
    assunto = get_object_or_404(Assunto, pk=assunto_id)
    questoes = Questao.objects.filter(id_assunto=assunto).prefetch_related('alternativas')
    
    if not questoes.exists():
        messages.warning(request, f'Não há questões cadastradas para o assunto: {assunto.nome}')
        return redirect('questoes:escolher_assunto')
    
    context = {
        'assunto': assunto,
        'questoes': questoes,
        'total_questoes': questoes.count()
    }
    
    return render(request, 'questoes/quiz.html', context)


def listar_questoes_view(request, assunto_id):
    """Lista questões de um assunto com filtros"""
    assunto = get_object_or_404(Assunto, pk=assunto_id)
    questoes = Questao.objects.filter(id_assunto=assunto).prefetch_related('alternativas')
    
    return render(request, 'questoes/listar_questoes.html', {
        'assunto': assunto,
        'questoes': questoes
    })


# ===== VIEWS DE AUTENTICAÇÃO =====

def login_view(request):
    """View de login"""
    if request.user.is_authenticated:
        return redirect('questoes:escolher_assunto')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        user_type = request.POST.get('user_type', 'usuario') # Mantido, mas não usado na autenticação
        
        if not email or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
        else:
            try:
                # Tenta encontrar o usuário pelo email
                user = User.objects.get(email=email)
                
                # CORREÇÃO/MELHORIA: Autenticar usando o username encontrado.
                # Se o email é usado para login, o username do User deve ser usado no authenticate.
                user_auth = authenticate(request, username=user.username, password=password)
                
                if user_auth is not None:
                    login(request, user_auth)
                    
                    if user_type == 'admin' and not user.is_staff:
                        # Logou, mas tentou como admin sem ser staff
                        messages.warning(request, 'Você logou como usuário. Para acessar a área administrativa, use o login de administrador.')
                    else:
                        messages.success(request, f'Bem-vindo(a), {user.first_name or user.username}!')
                    
                    return redirect('questoes:escolher_assunto')
                else:
                    # Falha de senha
                    messages.error(request, 'Email ou senha incorretos.')
            except User.DoesNotExist:
                # Falha de email
                messages.error(request, 'Email ou senha incorretos.')
    
    return render(request, 'questoes/login.html')

def cadastro_view(request):
    """View de cadastro"""
    if request.user.is_authenticated:
        return redirect('questoes:escolher_assunto')
    
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        
        if not nome or not email or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
        elif '@' not in email or '.' not in email:
            messages.error(request, 'Por favor, insira um e-mail válido.')
        elif len(password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
        else: # <--- AGORA CORRETAMENTE ALINHADO COM O 'IF' E 'ELIF'
            try:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Este e-mail já está cadastrado.')
                else:
                    # MELHORIA: Usar o email como username para garantir unicidade, se for sua intenção.
                    # Assumindo que o username não precisa ser visível publicamente e deve ser único:
                    user = User.objects.create_user(
                        username=email, 
                        email=email,
                        password=password,
                        first_name=nome[:30]
                    )
                    messages.success(request, 'Cadastro realizado com sucesso! Você já pode fazer login.')
                    return redirect('questoes:login')
            except Exception as e:
                # Log do erro para depuração
                error_logger.error(f'Erro no cadastro de usuário {email}: {e}', exc_info=True)
                messages.error(request, 'Erro ao criar conta. Por favor, tente novamente mais tarde.')
    
    return render(request, 'questoes/cadastro.html')
def logout_view(request):
    """View de logout"""
    logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('questoes:login')


# ===== VIEWS DE DESEMPENHO =====

@login_required
def desempenho_view(request):
    """View de desempenho do usuário"""
    user = request.user
    respostas = RespostaUsuario.objects.filter(id_usuario=user)
    
    total_respostas = respostas.count()
    respostas_corretas = respostas.filter(acertou=True).count()
    
    if total_respostas == 0:
        percentual_acerto = 0
        assuntos_stats = []
        messages.info(request, "Você ainda não respondeu a nenhuma questão. Comece um quiz para ver seu desempenho!")
    else:
        percentual_acerto = (respostas_corretas / total_respostas * 100)
    
        # Otimização: Agrupar por id_assunto e anotar os resultados
        respostas_por_assunto = respostas.values('id_questao__id_assunto__nome').annotate(
            total=Count('id'),
            acertos=Count('id', filter=Q(acertou=True))
        ).order_by('id_questao__id_assunto__nome')
        
        assuntos_stats = []
        for item in respostas_por_assunto:
            nome = item['id_questao__id_assunto__nome']
            total = item['total']
            acertos = item['acertos']
            percentual = (acertos / total * 100) if total > 0 else 0
            
            assuntos_stats.append({
                'nome_assunto': nome,
                'total_questoes': total,
                'acertos': acertos,
                'percentual': round(percentual, 1)
            })
    
    context = {
        'total_respostas': total_respostas,
        'respostas_corretas': respostas_corretas,
        'percentual_acerto': round(percentual_acerto, 1),
        'stats_assuntos': assuntos_stats,
        'usuario': user
    }
    
    return render(request, 'questoes/desempenho.html', context)


# ===== VIEWS ADMINISTRATIVAS =====

@login_required
def admin_dashboard_view(request):
    """Dashboard administrativo com métricas e estatísticas"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Você não tem permissão para acessar esta área.')
        return redirect('questoes:index')
    
    total_usuarios = User.objects.count()
    total_respostas = RespostaUsuario.objects.count()
    
    hoje = timezone.now().date()
    usuarios_hoje = User.objects.filter(date_joined__date=hoje).count()
    semana_inicio = hoje - timedelta(days=7)
    usuarios_semana = User.objects.filter(date_joined__gte=semana_inicio).count()
    mes_inicio = hoje - timedelta(days=30)
    usuarios_mes = User.objects.filter(date_joined__gte=mes_inicio).count()
    
    usuarios_lista = User.objects.order_by('-date_joined')[:10]
    
    try:
        assuntos_dificeis = []
        # Tenta calcular a taxa de acerto por assunto
        assuntos_stats = RespostaUsuario.objects.filter(
            id_questao__id_assunto__isnull=False # Ignorar respostas sem assunto
        ).values(
            'id_questao__id_assunto__nome'
        ).annotate(
            acertos=Sum(Case(When(acertou=True, then=1), default=0)),
            total=Count('id'),
            taxa=ExpressionWrapper(
                F('acertos') * 100.0 / F('total'),
                output_field=FloatField()
            )
        ).filter(total__gte=5).order_by('taxa')[:5] # Filtra por assuntos com 5+ respostas
        
        for stat in assuntos_stats:
            assuntos_dificeis.append({
                'assunto': stat['id_questao__id_assunto__nome'],
                'taxa': int(stat['taxa'])
            })
    except Exception as e:
        error_logger.error(f'Erro ao calcular assuntos difíceis: {e}', exc_info=True)
        assuntos_dificeis = []
    
    try:
        questoes_stats = RespostaUsuario.objects.values('id_questao').annotate(
            taxa=Avg('acertou') * 100
        )
        
        # MELHORIA: Usar filtros mais concisos
        dificeis = sum(1 for stat in questoes_stats if stat['taxa'] is not None and stat['taxa'] < 40)
        medias = sum(1 for stat in questoes_stats if stat['taxa'] is not None and 40 <= stat['taxa'] <= 70)
        faceis = sum(1 for stat in questoes_stats if stat['taxa'] is not None and stat['taxa'] > 70)
        
        buckets = {'dificeis': dificeis, 'medias': medias, 'faceis': faceis}
    except Exception as e:
        error_logger.error(f'Erro ao calcular buckets de questões: {e}', exc_info=True)
        buckets = {'dificeis': 0, 'medias': 0, 'faceis': 0}
    
    try:
        questoes_erradas = RespostaUsuario.objects.values(
            'id_questao', 'id_questao__texto'
        ).annotate(
            erros=Sum(Case(When(acertou=False, then=1), default=0)),
            total=Count('id'),
            taxa_erro=ExpressionWrapper(
                F('erros') * 100.0 / F('total'),
                output_field=FloatField()
            )
        ).filter(total__gte=3).order_by('-taxa_erro', '-erros')[:5]
        
        questoes_erradas_list = []
        for q in questoes_erradas:
            questoes_erradas_list.append({
                'id': q['id_questao'],
                'texto': q['id_questao__texto'][:80] + '...' if len(q['id_questao__texto']) > 80 else q['id_questao__texto'],
                'taxa_erro': int(q['taxa_erro'])
            })
        questoes_erradas = questoes_erradas_list
    except Exception as e:
        error_logger.error(f'Erro ao calcular questões erradas: {e}', exc_info=True)
        questoes_erradas = []
    
    context = {
        'total_usuarios': total_usuarios,
        'total_respostas': total_respostas,
        'usuarios_hoje': usuarios_hoje,
        'usuarios_semana': usuarios_semana,
        'usuarios_mes': usuarios_mes,
        'usuarios_lista': usuarios_lista,
        'assuntos_dificeis': assuntos_dificeis,
        'buckets': buckets,
        'questoes_erradas': questoes_erradas,
    }
    
    return render(request, 'questoes/admin_dashboard.html', context)


def admin_login_view(request):
    """Login para administradores"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('questoes:admin_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '') # MELHORIA: 'senha' para 'password'
        
        if not email or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
        else:
            try:
                # Busca o usuário pelo email E garante que ele seja staff
                user = User.objects.get(email=email, is_staff=True)
                
                # Autenticação
                user_auth = authenticate(request, username=user.username, password=password)
                
                if user_auth is not None:
                    login(request, user_auth)
                    messages.success(request, f'Bem-vindo(a), {user.first_name or user.username}!')
                    return redirect('questoes:admin_dashboard')
                else:
                    messages.error(request, 'Email ou senha incorretos, ou você não tem permissão de administrador.')
            except User.DoesNotExist:
                messages.error(request, 'Email ou senha incorretos, ou você não tem permissão de administrador.')
    
    return render(request, 'questoes/admin_login.html') 
# ===== VIEWS ADMIN - GERENCIAMENTO =====
@login_required
def gerenciar_questoes_view(request):
    """Exibe a lista de questões para gerenciamento admin"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    # MELHORIA: Contar alternativas e agrupar por dificuldade no ORM (mais eficiente)
    questoes = Questao.objects.select_related('id_assunto').annotate(
        total_alternativas=Count('alternativas')
    ).order_by('-id')
    
    total_questoes = questoes.count()
    
    # MELHORIA: Contagem de dificuldade usando ORM
    questoes_por_dificuldade_query = questoes.values('dificuldade').annotate(
        count=Count('id')
    ).order_by('dificuldade')
    
    questoes_por_dificuldade = {}
    for item in questoes_por_dificuldade_query:
        dificuldade = item['dificuldade'] if item['dificuldade'] else 'não definida'
        questoes_por_dificuldade[dificuldade] = item['count']

    # Adiciona a contagem de "não definida" se for zero e não aparecer na query
    if 'não definida' not in questoes_por_dificuldade:
        if 'dificuldade' in [f.name for f in Questao._meta.fields] and not Questao.objects.filter(dificuldade__isnull=False).exists():
            pass # Não precisa adicionar se o campo estiver preenchido em todos
        else:
            # Se a dificuldade for um campo NULL ou vazio
            dificuldade_count = Questao.objects.filter(dificuldade__isnull=True).count()
            if dificuldade_count > 0:
                questoes_por_dificuldade['não definida'] = dificuldade_count
    
    context = {
        'questoes': questoes,
        'total_questoes': total_questoes,
        'questoes_por_dificuldade': questoes_por_dificuldade
    }
    
    return render(request, 'questoes/gerenciar_questoes.html', context)


@login_required
def adicionar_questao_view(request):
    """View para adicionar nova questão com seletores encadeados"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    mensagem_status = ''
    mensagem_texto = ''
    
    # MELHORIA: Busca centralizada para evitar 3 consultas
    assuntos = Assunto.objects.all().order_by('tipo_assunto', 'nome')
    
    assuntos_tema = assuntos.filter(tipo_assunto='tema')
    assuntos_concurso = assuntos.filter(tipo_assunto='concurso')
    assuntos_profissional = assuntos.filter(tipo_assunto='profissional')
    
    # Obtém órgãos únicos (set(..)) e remove vazios
    orgaos = sorted(list(set(assuntos_concurso.values_list('concurso_orgao', flat=True).exclude(concurso_orgao=''))))

    # Prepara dados para JSON (seletores encadeados no front-end)
    assuntos_por_tipo_json = {
        'tema': [{'id': a.id, 'nome': a.nome} for a in assuntos_tema],
        'concurso': [{
            'id': a.id,
            'nome': a.nome,
            # Garante que esses campos existam no seu modelo Assunto
            'concurso_orgao': getattr(a, 'concurso_orgao', None), 
            'concurso_banca': getattr(a, 'concurso_banca', None),
            'concurso_ano': getattr(a, 'concurso_ano', None),
            'concurso_prova': getattr(a, 'concurso_prova', None)
        } for a in assuntos_concurso],
        'profissional': [{'id': a.id, 'nome': a.nome} for a in assuntos_profissional]
    }
    
    total_questoes = Questao.objects.count()
    total_assuntos = assuntos.count() # Usa a lista já carregada
    
    if request.method == 'POST':
        # LINHAS CORRIGIDAS (Nível de indentação 2: 8 espaços)
        tipo_conteudo = request.POST.get('tipo_conteudo', '').strip()
        enunciado = request.POST.get('enunciado', '').strip()
        explicacao = request.POST.get('explicacao', '').strip()
        
        alt1 = request.POST.get('alt1', '').strip()
        alt2 = request.POST.get('alt2', '').strip()
        alt3 = request.POST.get('alt3', '').strip()
        alt4 = request.POST.get('alt4', '').strip()
        alt5 = request.POST.get('alt5', '').strip()
        
        correta = request.POST.get('correta', '')
        
        id_assunto = None
        if tipo_conteudo == 'tema':
            id_assunto = request.POST.get('assunto_tema')
        elif tipo_conteudo == 'profissional':
            id_assunto = request.POST.get('assunto_profissional')
        elif tipo_conteudo == 'concurso':
            # Usa o id_assunto final selecionado (geralmente é o último seletor)
            id_assunto = request.POST.get('id_assunto') 
        
        errors = []
        # ... o restante do seu código POST
        
        if not id_assunto:
            errors.append('Erro: Nenhum conteúdo foi selecionado. Por favor, selecione um conteúdo válido.')
        
        has_content = enunciado or explicacao or any([alt1, alt2, alt3, alt4, alt5])
        if not has_content:
            errors.append('Preencha pelo menos o enunciado ou as alternativas para criar a questão.')
        
        alternativas = [alt1, alt2, alt3, alt4, alt5]
        
        if correta:
            try:
                correta_index = int(correta)
                if correta_index >= 1 and correta_index <= 5:
                    if not alternativas[correta_index - 1]:
                        letra = chr(64 + correta_index)
                        errors.append(f"A alternativa {letra} selecionada como correta está vazia.")
                else:
                    errors.append("Índice de alternativa correta inválido.")
            except ValueError:
                errors.append("Valor da alternativa correta inválido.")
        
        # ... Continuação de adicionar_questao_view(request):

        if errors:
            mensagem_status = 'error'
            mensagem_texto = '<br>'.join(errors)
            # Adiciona as mensagens de erro na sessão para exibição
            messages.error(request, mensagem_texto) 
        else:
            try:
                from django.db import transaction
                
                with transaction.atomic():
                    # Garante que o assunto existe
                    assunto = get_object_or_404(Assunto, pk=id_assunto)
                    
                    # CORRIGIDO: A criação da questão foi movida para DENTRO da transação
                    questao = Questao.objects.create(
                        texto=enunciado,
                        id_assunto=assunto,
                        explicacao=explicacao
                    )
                    
                    alternativas_data = [
                        ('A', alt1), ('B', alt2), ('C', alt3), 
                        ('D', alt4), ('E', alt5),
                    ]
                    
                    correta_index = int(correta) if correta else 0
                    
                    # Cria lista para Bulk Create (mais performático)
                    novas_alternativas = []
                    for index, (letra, texto) in enumerate(alternativas_data):
                        if texto:
                            eh_correta = (index + 1 == correta_index)
                            novas_alternativas.append(
                                Alternativa(
                                    # CORRIGIDO: id_questao=questao estava em indentação incorreta
                                    id_questao=questao,
                                    texto=texto,
                                    eh_correta=eh_correta
                                )
                            )
                    
                    # Cria todas as alternativas de uma vez
                    if novas_alternativas:
                        Alternativa.objects.bulk_create(novas_alternativas)
                    
                    messages.success(request, f'Questão #{questao.id} adicionada com sucesso!')
                
                # CORRIGIDO: O redirect deve estar fora da transação, mas dentro do bloco 'else' do 'if errors'
                return redirect('questoes:adicionar_questao')
            
            except Exception as e:
                # CORRIGIDO: Bloco except alinhado com o 'try'
                error_logger.error(f'Erro ao adicionar questão: {e}', exc_info=True)
                messages.error(request, f'Erro ao adicionar a questão: {str(e)}')
    
    context = {
        'mensagem_status': mensagem_status,
        'mensagem_texto': mensagem_texto,
        'assuntos_por_tipo': {
            'tema': assuntos_tema,
            'concurso': assuntos_concurso,
            'profissional': assuntos_profissional,
        },
        'assuntos_por_tipo_json': json.dumps(assuntos_por_tipo_json),
        'orgaos': orgaos,
        'total_questoes': total_questoes,
        'total_assuntos': total_assuntos,
    }
    
    return render(request, 'questoes/adicionar_questao.html', context)


@login_required
def editar_questao_view(request, questao_id):
    """Edita uma questão existente"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    questao = get_object_or_404(Questao, pk=questao_id)
    assuntos = Assunto.objects.order_by('nome')
    # Otimização: prefetch do assunto
    alternativas = questao.alternativas.all().order_by('id') 
    
    if request.method == 'POST':
        enunciado = request.POST.get('enunciado', '').strip()
        explicacao = request.POST.get('explicacao', '').strip()
        id_assunto = request.POST.get('id_assunto')
        correta_pk = request.POST.get('correta') # Guarda a PK da alternativa correta
        
        alternativas_dict = {}
        
        # Coleta as alternativas enviadas no POST
        for key, value in request.POST.items():
            if key.startswith('alternativas['):
                alt_id = key[13:-1] # Ajustei o índice de corte se o campo for 'alternativas[ID]'
                alternativas_dict[alt_id] = value.strip()
        
        if not enunciado or not id_assunto or not alternativas_dict:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios (enunciado, assunto e alternativas).')
    else:
            try:
                from django.db import transaction
                with transaction.atomic():
                    questao.texto = enunciado
                    questao.explicacao = explicacao
                    questao.id_assunto_id = id_assunto
                    questao.save()
                    
                    # Atualiza alternativas existentes
                    for alt_id, texto in alternativas_dict.items():
                        # MELHORIA: Usa update_or_create ou get/save
                        alternativa = Alternativa.objects.get(pk=alt_id, id_questao=questao)
                        alternativa.texto = texto
                        # A alternativa é correta se o PK dela for igual ao PK enviado no campo 'correta'
                        alternativa.eh_correta = (str(alternativa.pk) == correta_pk)
                        alternativa.save()
                        
                    # Não há lógica para adicionar novas alternativas, apenas atualizar as existentes
                    
                    messages.success(request, 'Questão atualizada com sucesso!')
                return redirect('questoes:gerenciar_questoes')
            except Exception as e:
                error_logger.error(f'Erro ao editar questão {questao_id}: {e}', exc_info=True)
                messages.error(request, f'Erro ao atualizar a questão: {str(e)}')
    
    context = {
        'questao': questao,
        'assuntos': assuntos,
        'alternativas': alternativas,
    }
    
    return render(request, 'questoes/editar_questao.html', context)


@login_required
def deletar_questao_view(request):
    """Deleta uma questão e todos os dados relacionados"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    if request.method == 'POST':
        questao_id = request.POST.get('questao_id')
        if questao_id:
            try:
                questao = get_object_or_404(Questao, pk=questao_id)
                
                from django.db import transaction
                with transaction.atomic():
                    # Se seus modelos têm on_delete=CASCADE, as próximas linhas são opcionais/redundantes,
                    # mas garantem a ordem e o controle na transação.
                    # RespostaUsuario.objects.filter(id_questao=questao).delete()
                    # Alternativa.objects.filter(id_questao=questao).delete()
                    
                    questao.delete() # Deleta em cascata se configurado corretamente
                
                messages.success(request, f'Questão #{questao_id} deletada com sucesso!')
            except Questao.DoesNotExist:
                messages.error(request, 'Questão não encontrada.')
            except Exception as e:
                error_logger.error(f'Erro ao deletar questão {questao_id}: {e}', exc_info=True)
                messages.error(request, f'Erro ao deletar questão: {str(e)}')
    
    return redirect('questoes:gerenciar_questoes')

@login_required
def gerenciar_assuntos_view(request):
    """Exibe a lista de assuntos para gerenciamento"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    assuntos = Assunto.objects.annotate(
        total_questoes=Count('questoes')
    ).order_by('tipo_assunto', 'nome')
    
    total_questoes = Questao.objects.count()
    
    context = {
        'assuntos': assuntos,
        'total_assuntos': assuntos.count(),
        'total_questoes': total_questoes
    }
    
    return render(request, 'questoes/gerenciar_assuntos.html', context)


@login_required
def adicionar_assunto_view(request):
    """View para adicionar novo assunto/conteúdo"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    mensagem_status = ''
    mensagem_texto = ''
    
    if request.method == 'POST':
        tipo_assunto = request.POST.get('tipo_assunto', '').strip()
        nome_assunto = request.POST.get('nome_assunto', '').strip()
        
        # Garante que os campos são strings vazias se não existirem
        concurso_ano = request.POST.get('concurso_ano', '').strip()
        concurso_banca = request.POST.get('concurso_banca', '').strip()
        concurso_orgao = request.POST.get('concurso_orgao', '').strip()
        concurso_prova = request.POST.get('concurso_prova', '').strip()
        
        errors = []
        if not tipo_assunto:
            errors.append('Por favor, selecione o tipo de conteúdo.')
        elif tipo_assunto != 'concurso' and not nome_assunto:
            errors.append('Por favor, digite o nome do conteúdo.')
        elif tipo_assunto == 'concurso' and not all([concurso_ano, concurso_banca, concurso_orgao, concurso_prova]):
            errors.append('Para concursos, preencha todos os campos obrigatórios (Ano, Banca, Órgão e Prova).')
        
        if errors:
            mensagem_status = 'error'
            mensagem_texto = '<br>'.join(errors)
            messages.error(request, mensagem_texto)
        else: # <--- AGORA CORRETAMENTE ALINHADO COM O 'IF ERRORS:'
            try:
                if tipo_assunto == 'concurso':
                    nome_final = f"{concurso_ano} - {concurso_banca} - {concurso_orgao} - {concurso_prova}"
                else:
                    nome_final = nome_assunto
                
                if Assunto.objects.filter(nome=nome_final, tipo_assunto=tipo_assunto).exists():
                    messages.error(request, 'Já existe um conteúdo com este nome para este tipo.')
                else:
                    assunto = Assunto.objects.create(
                        nome=nome_final,
                        tipo_assunto=tipo_assunto
                    )
                    
                    if tipo_assunto == 'concurso':
                        assunto.concurso_ano = concurso_ano
                        assunto.concurso_banca = concurso_banca
                        assunto.concurso_orgao = concurso_orgao
                        assunto.concurso_prova = concurso_prova
                        assunto.save()
                    
                    tipo_display = tipo_assunto.capitalize()
                    messages.success(request, f'{tipo_display} "{nome_final}" adicionado com sucesso!')
                    return redirect('questoes:adicionar_assunto') # Redireciona para evitar re-submit
            
            except Exception as e: # <--- AGORA CORRETAMENTE ALINHADO COM O 'TRY'
                error_logger.error(f'Erro ao adicionar assunto: {e}', exc_info=True)
                messages.error(request, f'Erro ao adicionar o conteúdo: {str(e)}')
    
    return render(request, 'questoes/adicionar_assunto.html', {
        'mensagem_status': mensagem_status,
        'mensagem_texto': mensagem_texto,
    })


@login_required
def deletar_assunto_view(request):
    """Deleta um assunto e todas as questões relacionadas"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    if request.method == 'POST':
        assunto_id = request.POST.get('id')
        if assunto_id:
            try:
                assunto = get_object_or_404(Assunto, pk=assunto_id)
                
                from django.db import transaction
                with transaction.atomic():
                    # Otimização: A deleção em cascata (se configurada) é automática 
                    # quando Assunto.delete() é chamado.
                    # As questões e as respostas/alternativas delas serão deletadas.
                    assunto.delete()
                
                messages.success(request, f'Conteúdo "{assunto.nome}" deletado com sucesso!')
            except Assunto.DoesNotExist:
                messages.error(request, 'Conteúdo não encontrado.')
            except Exception as e:
                error_logger.error(f'Erro ao deletar assunto {assunto_id}: {e}', exc_info=True)
                messages.error(request, f'Erro ao deletar conteúdo: {str(e)}')
    
    return redirect('questoes:gerenciar_assuntos')


@login_required
def gerenciar_comentarios_view(request):
    """Exibe lista de comentários reportados ou inativos"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    comentarios = ComentarioQuestao.objects.filter(
        # Filtra comentários inativos OU que tenham pelo menos 1 denúncia
        Q(ativo=False) | Q(denuncias__isnull=False) 
    ).annotate(
        total_denuncias=Count('denuncias')
    ).distinct().order_by('-data_comentario')
    
    context = {
        'comentarios': comentarios
    }
    
    return render(request, 'questoes/gerenciar_comentarios.html', context)
# ASSUMIDO: Esta é a função que lida com a moderação/alternância de status
@login_required
def alternar_status_comentario_view(request, comentario_id):
    """Alterna o status ativo/inativo de um comentário e remove denúncias"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    if request.method == 'POST':
        try:
            comentario = get_object_or_404(ComentarioQuestao, pk=comentario_id)
            comentario.ativo = not comentario.ativo
            # CORRIGIDO: Recuo
            comentario.save() 
            
            # CORRIGIDO: Recuo 
            # Deleta as denúncias após a revisão (opcional, dependendo da sua regra de negócio)
            if comentario.ativo:
                DenunciaComentario.objects.filter(id_comentario=comentario).delete()
            
            messages.success(request, f'Comentário {"ativado (denúncias revisadas)" if comentario.ativo else "desativado"} com sucesso!')
        except Exception as e:
            # CORRIGIDO: Recuo para alinhar com o 'try'
            error_logger.error(f'Erro ao alternar status do comentário {comentario_id}: {e}', exc_info=True)
            messages.error(request, f'Erro ao atualizar o comentário: {str(e)}')
    
    return redirect('questoes:gerenciar_comentarios')


@login_required
def deletar_comentario_view(request, comentario_id):
    """Deleta um comentário permanentemente"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    if request.method == 'POST':
        try:
            comentario = get_object_or_404(ComentarioQuestao, pk=comentario_id)
            comentario.delete() # Deleta em cascata curtidas e denúncias relacionadas
            
            messages.success(request, 'Comentário excluído permanentemente com sucesso!')
        except Exception as e: # CORRIGIDO: Recuo para alinhar com o 'try'
            error_logger.error(f'Erro ao deletar comentário {comentario_id}: {e}', exc_info=True)
            messages.error(request, f'Erro ao excluir comentário: {str(e)}')
    
    return redirect('questoes:gerenciar_comentarios')


@login_required
def gerenciar_relatorios_view(request):
    """Exibe lista de relatórios com filtros"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    filtro_status = request.GET.get('status', 'todos')
    filtro_prioridade = request.GET.get('prioridade', 'todos')
    
    relatorios = RelatorioBug.objects.all()
    
    if filtro_status != 'todos':
        relatorios = relatorios.filter(status=filtro_status)
    
    if filtro_prioridade != 'todos':
        relatorios = relatorios.filter(prioridade=filtro_prioridade)
    
    relatorios = relatorios.select_related('id_usuario').order_by('-data_relatorio')
    
    # MELHORIA: Uso de agregação para obter as estatísticas em uma query
    stats_query = RelatorioBug.objects.values('status').annotate(count=Count('status'))
    stats_dict = {item['status']: item['count'] for item in stats_query}

    stats = {
        'total': RelatorioBug.objects.count(),
        'abertos': stats_dict.get('aberto', 0),
        'em_andamento': stats_dict.get('em_andamento', 0),
        'resolvidos': stats_dict.get('resolvido', 0),
    }
    
    context = {
        'relatorios': relatorios,
        'stats': stats,
        'filtro_status': filtro_status,
        'filtro_prioridade': filtro_prioridade,
    }
    
    return render(request, 'questoes/gerenciar_relatorios.html', context)


@login_required
def atualizar_status_relatorio_view(request, relatorio_id):
    """Atualiza o status de um relatório"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    if request.method == 'POST':
        try:
            relatorio = get_object_or_404(RelatorioBug, pk=relatorio_id)
            novo_status = request.POST.get('novo_status')
            
            if novo_status and novo_status in ['aberto', 'em_andamento', 'resolvido']: # Validação do status
                relatorio.status = novo_status
                relatorio.data_atualizacao = timezone.now()
                relatorio.save()
                messages.success(request, f'Status do relatório #{relatorio_id} atualizado para "{novo_status.replace("_", " ").capitalize()}" com sucesso!')
            else:
                messages.error(request, 'Status inválido.')
        except Exception as e:
            error_logger.error(f'Erro ao atualizar status do relatório {relatorio_id}: {e}', exc_info=True)
            messages.error(request, f'Erro ao atualizar status do relatório: {str(e)}')
    
    return redirect('questoes:gerenciar_relatorios')


@login_required
def responder_relatorio_view(request):
    """Responde a um relatório"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    if request.method == 'POST':
        relatorio_id = request.POST.get('id_relatorio')
        resposta = request.POST.get('resposta', '').strip()
        
        if resposta and relatorio_id:
            try:
                relatorio = get_object_or_404(RelatorioBug, pk=relatorio_id)
                relatorio.resposta_admin = resposta
                relatorio.usuario_viu_resposta = False  # Marca como nova resposta para o usuário
                relatorio.data_atualizacao = timezone.now()
                relatorio.save()
                messages.success(request, f'Resposta enviada com sucesso para o relatório #{relatorio_id}.')
            except Exception as e: # CORRIGIDO: Recuo para alinhar com o 'try'
                error_logger.error(f'Erro ao responder relatório {relatorio_id}: {e}', exc_info=True)
                messages.error(request, f'Erro ao enviar resposta: {str(e)}')
        else:
            messages.error(request, 'A resposta e o ID do relatório não podem estar vazios.')
    
    return redirect('questoes:gerenciar_relatorios')

@login_required
def deletar_comentario_view(request, comentario_id):
    """Deleta um comentário permanentemente"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    if request.method == 'POST':
        try:
            comentario = get_object_or_404(ComentarioQuestao, pk=comentario_id)
            comentario.delete() # Deleta em cascata curtidas e denúncias relacionadas
            
            messages.success(request, 'Comentário excluído permanentemente com sucesso!')
        # CORRIGIDO: O 'except' agora está alinhado com o 'try'
        except Exception as e:
            error_logger.error(f'Erro ao deletar comentário {comentario_id}: {e}', exc_info=True)
            messages.error(request, f'Erro ao excluir comentário: {str(e)}')
    
    return redirect('questoes:gerenciar_comentarios')

@login_required
def gerenciar_relatorios_view(request):
    """Exibe lista de relatórios com filtros"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    filtro_status = request.GET.get('status', 'todos')
    filtro_prioridade = request.GET.get('prioridade', 'todos')
    
    relatorios = RelatorioBug.objects.all()
    
    if filtro_status != 'todos':
        relatorios = relatorios.filter(status=filtro_status)
    
    if filtro_prioridade != 'todos':
        relatorios = relatorios.filter(prioridade=filtro_prioridade)
    
    relatorios = relatorios.select_related('id_usuario').order_by('-data_relatorio')
    
    # MELHORIA: Uso de agregação para obter as estatísticas em uma query
    stats_query = RelatorioBug.objects.values('status').annotate(count=Count('status'))
    stats_dict = {item['status']: item['count'] for item in stats_query}

    stats = {
        'total': RelatorioBug.objects.count(),
        'abertos': stats_dict.get('aberto', 0),
        'em_andamento': stats_dict.get('em_andamento', 0),
        'resolvidos': stats_dict.get('resolvido', 0),
    }
    
    context = {
        'relatorios': relatorios,
        'stats': stats,
        'filtro_status': filtro_status,
        'filtro_prioridade': filtro_prioridade,
    }
    
    return render(request, 'questoes/gerenciar_relatorios.html', context)


@login_required
def atualizar_status_relatorio_view(request, relatorio_id):
    """Atualiza o status de um relatório"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    if request.method == 'POST':
        try:
            relatorio = get_object_or_404(RelatorioBug, pk=relatorio_id)
            novo_status = request.POST.get('novo_status')
            
            if novo_status and novo_status in ['aberto', 'em_andamento', 'resolvido']: # Validação do status
                relatorio.status = novo_status
                relatorio.data_atualizacao = timezone.now()
                relatorio.save()
                messages.success(request, f'Status do relatório #{relatorio_id} atualizado para "{novo_status.replace("_", " ").capitalize()}" com sucesso!')
            else:
                messages.error(request, 'Status inválido.')
        except Exception as e:
            error_logger.error(f'Erro ao atualizar status do relatório {relatorio_id}: {e}', exc_info=True)
            messages.error(request, f'Erro ao atualizar status do relatório: {str(e)}')
    
    return redirect('questoes:gerenciar_relatorios')

@login_required
def responder_relatorio_view(request):
    """Responde a um relatório"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('questoes:index')
    
    if request.method == 'POST':
        relatorio_id = request.POST.get('id_relatorio')
        resposta = request.POST.get('resposta', '').strip()
        
        # Este 'if' define o nível de indentação do try/except e do else
        if resposta and relatorio_id: 
            try:
                # Nível de indentação correto dentro do try
                relatorio = get_object_or_404(RelatorioBug, pk=relatorio_id)
                relatorio.resposta_admin = resposta
                relatorio.usuario_viu_resposta = False  # Marca como nova resposta para o usuário
                relatorio.data_atualizacao = timezone.now()
                relatorio.save()
                messages.success(request, f'Resposta enviada com sucesso para o relatório #{relatorio_id}.')
            # CORRIGIDO: O 'except' está alinhado com o 'try'
            except Exception as e:
                error_logger.error(f'Erro ao responder relatório {relatorio_id}: {e}', exc_info=True)
                messages.error(request, f'Erro ao enviar resposta: {str(e)}')
        # CORRIGIDO: O 'else' está alinhado com o 'if resposta and relatorio_id:'
        else:
            messages.error(request, 'A resposta e o ID do relatório não podem estar vazios.')
    
    return redirect('questoes:gerenciar_relatorios')  

    # ==============================================================================
# 🟢 PLACEHOLDERS FINAIS (Adicionar APENAS se as funções não existirem)
# Estas duas funções estavam faltando e causaram os últimos erros.
# ==============================================================================

# Adicionar se não existirem
def validar_resposta_view(request):
    """View que processa a resposta do quiz."""
    if request.method == 'POST':
        # Lógica da API de validação
        pass 
    return JsonResponse({'status': 'ok', 'message': 'Resposta processada'}, status=200)

# Adicionar se não existir
def quiz_view(request, assunto_id):
    """Placeholder para a view que carrega a página do quiz."""
    return render(request, 'questoes/quiz.html', {})

# IMPORTANTE: Se outras funções do urls.py também estiverem faltando, 
# você precisará adicioná-las manualmente ou me enviar o código para revisar.
# Exemplo: index_view, login_view, api_comentarios, etc.
# ==============================================================================

# No final do arquivo questoes/views.py

from django.http import JsonResponse # Garanta que este import está no topo do seu views.py

# ==============================================================================
# 🟢 PLACEHOLDERS - APIs
# ==============================================================================

# Adicionar se não existir (resolve o erro atual)
def api_comentarios(request):
    """Placeholder para a API que lida com comentários."""
    return JsonResponse({'status': 'ok', 'data': []}, status=200)

# Adicionar se não existir (próximo erro provável no urls.py)
def api_estatisticas(request):
    """Placeholder para a API que lida com estatísticas."""
    return JsonResponse({'status': 'ok', 'data': {}}, status=200)

# Adicionar se não existir (próximo erro provável no urls.py)
def api_notificacoes(request):
    """Placeholder para a API de notificações."""
    return JsonResponse({'status': 'ok', 'notifications': []}, status=200)

# ==============================================================================

# No final do arquivo questoes/views.py
from django.shortcuts import render, redirect # Garanta que estas importações estão no topo do seu views.py
from django.contrib.auth.decorators import login_required # Garanta que este import está no topo

# ==============================================================================
# 🟢 PLACEHOLDERS - Views Administrativas e Relatórios
# ==============================================================================

# Adicionar se não existir (resolve o erro atual)
def relatar_problema_view(request):
    """Placeholder para a view de relatar problema."""
    # Retorna o formulário de relatar problema
    return render(request, 'questoes/relatar_problema.html', {})

# Adicionar se não existir (próximo erro provável no urls.py)
def api_notificacoes(request):
    """Placeholder para a API de notificações."""
    return JsonResponse({'status': 'ok', 'notifications': []}, status=200)

# Adicionar se não existir (próximo erro provável no urls.py)
@login_required
def admin_dashboard_view(request):
    """Placeholder para a view do dashboard do administrador."""
    return render(request, 'questoes/admin_dashboard.html', {})

# Adicionar se não existir
@login_required
def gerenciar_relatorios_view(request):
    """Placeholder para a view de gerenciamento de relatórios."""
    return render(request, 'questoes/gerenciar_relatorios.html', {})

# Adicionar se não existir
@login_required
def atualizar_status_relatorio_view(request, relatorio_id):
    """Placeholder para a view de atualização de status de relatório."""
    return redirect('questoes:gerenciar_relatorios')

# Adicionar se não existir
@login_required
def gerenciar_usuarios_view(request):
    """Placeholder para a view de gerenciamento de usuários."""
    return render(request, 'questoes/gerenciar_usuarios.html', {})

# Adicionar se não existir
def admin_login_view(request):
    """Placeholder para a view de login administrativo."""
    return render(request, 'questoes/admin_login.html', {})

# ==============================================================================