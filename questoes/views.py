from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q, Sum, Avg, Case, When, IntegerField, FloatField, F, ExpressionWrapper, Max, OuterRef, Subquery
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta
from collections import Counter
import json
import logging
from django.views.decorators.http import require_POST
# Importação necessária para transações (usada em adicionar_questao_view)
from django.db import transaction 
# Certifique-se de que get_object_or_404 e JsonResponse estão importados
from .models import (
    Assunto, Questao, Alternativa, RespostaUsuario,
    ComentarioQuestao, CurtidaComentario, DenunciaComentario,
    RelatorioBug
)
from .filters import QuestaoFilter

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
## ===== VIEWS DE QUIZ/QUESTÕES =====

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
    """
    Lista questões de um assunto. A filtragem de exibição é delegada ao JS.
    O backend apenas calcula e associa o STATUS de cada questão.
    """
    assunto = get_object_or_404(Assunto, pk=assunto_id)
    
    # Captura o filtro da URL (apenas para fins de contexto, a lógica principal de filtro fica no JS)
    filtro = request.GET.get('filtro', 'todas')
    
    # Busca o usuário logado
    user_id = request.user.id if request.user.is_authenticated else None
    
    # Query inicial: questões relacionadas ao assunto selecionado
    queryset = Questao.objects.filter(id_assunto=assunto).select_related('id_assunto')
    
    # Aplicar filtros de busca do django-filter (texto, tipo_assunto, assunto)
    questao_filter = QuestaoFilter(request.GET, queryset=queryset)
    questoes = questao_filter.qs
    
    questoes_ids = list(questoes.values_list('id', flat=True))
    
    # Prepara lista de questões com status
    questoes_com_status = []
    respostas_dict = {}
    
    if user_id:
        # Busca a ÚLTIMA resposta de cada questão do usuário
        # Abordagem: Para cada questão, pega a resposta com a data mais recente
        
        # Primeiro, pega a data máxima de resposta para cada questão
        respostas_agrupadas = RespostaUsuario.objects.filter(
            id_usuario_id=user_id,
            id_questao__in=questoes_ids
        ).values('id_questao').annotate(
            max_data=Max('data_resposta')
        )
        
        # Monta um dicionário com questão_id -> max_data
        questoes_com_data_maxima = {}
        for item in respostas_agrupadas:
            questoes_com_data_maxima[item['id_questao']] = item['max_data']
        
        # Busca a última resposta de cada questão usando a data máxima
        # OTIMIZAÇÃO: Busca todas as respostas com as datas máximas em uma única query
        if questoes_com_data_maxima:
            # Monta lista de condições para busca eficiente
            conditions = Q()
            for questao_id, max_data in questoes_com_data_maxima.items():
                conditions |= Q(id_questao_id=questao_id, data_resposta=max_data)
            
            # Busca todas as últimas respostas de uma vez
            ultimas_respostas_query = RespostaUsuario.objects.filter(
                id_usuario_id=user_id
            ).filter(conditions).order_by('id_questao_id', '-id')
            
            # Popula o dicionário (pega apenas a primeira resposta de cada questão)
            questoes_processadas = set()
            for resposta in ultimas_respostas_query:
                questao_id = resposta.id_questao.id
                if questao_id not in questoes_processadas:
                    respostas_dict[questao_id] = bool(resposta.acertou)
                    questoes_processadas.add(questao_id)
    
    # Monta lista de questões com status baseado na última resposta (CORRIGIDO: SEM PRÉ-FILTRAGEM)
    for questao in questoes:
        status = 'nao-respondida'
        classe_status = 'nao-respondida'
        
        if questao.id in respostas_dict:
            acertou = bool(respostas_dict[questao.id])  # Garante booleano
            if acertou:
                status = 'certa'
                classe_status = 'certa'
            else:
                status = 'errada'
                classe_status = 'errada'
        
        # O objeto é adicionado INCONDICIONALMENTE
        questoes_com_status.append({
            'questao': questao,
            'status': status,
            'classe_status': classe_status
        })

    # Calcula contadores (Esta lógica deve permanecer, pois é a contagem real dos stats)
    total_todas = questoes.count()
    
    if user_id:
        # Contador: Respondidas (questões respondidas pelo menos uma vez)
        respondidas_ids = RespostaUsuario.objects.filter(
            id_usuario_id=user_id,
            id_questao__in=questoes_ids
        ).values_list('id_questao', flat=True).distinct()
        total_respondidas = len(respondidas_ids)
        
        # Contador: Não Respondidas (diferença entre total e respondidas)
        total_nao_respondidas = total_todas - total_respondidas
        
        # Contador: Certas e Erradas
        total_certas = 0
        total_erradas = 0
        
        for questao_id in questoes_ids:
            if questao_id in respostas_dict:
                acertou = bool(respostas_dict[questao_id])  # Garante booleano
                if acertou:  # acertou = True
                    total_certas += 1
                else:  # acertou = False
                    total_erradas += 1
    else:
        total_respondidas = 0
        total_nao_respondidas = total_todas
        total_certas = 0
        total_erradas = 0
    
    # Calcula porcentagens para as barras de progresso
    porcentagem_nao_respondidas = (total_nao_respondidas / total_todas * 100) if total_todas > 0 else 0
    porcentagem_respondidas = (total_respondidas / total_todas * 100) if total_todas > 0 else 0
    porcentagem_certas = (total_certas / total_respondidas * 100) if total_respondidas > 0 else 0
    porcentagem_erradas = (total_erradas / total_respondidas * 100) if total_respondidas > 0 else 0
    porcentagem_taxa_acerto = (total_certas / total_respondidas * 100) if total_respondidas > 0 else 0
    porcentagem_progresso_geral = (total_respondidas / total_todas * 100) if total_todas > 0 else 0
    
    stats = {
        'todas': total_todas,
        'respondidas': total_respondidas,
        'nao_respondidas': total_nao_respondidas,
        'certas': total_certas,
        'erradas': total_erradas,
        'porcentagens': {
            'nao_respondidas': round(porcentagem_nao_respondidas, 1),
            'respondidas': round(porcentagem_respondidas, 1),
            'certas': round(porcentagem_certas, 1),
            'erradas': round(porcentagem_erradas, 1),
            'taxa_acerto': round(porcentagem_taxa_acerto, 1),
            'progresso_geral': round(porcentagem_progresso_geral, 1)
        }
    }
    
    # ATENÇÃO: Se estiver usando o código que eu gerei anteriormente, ele já tem a lógica de stats.
    # Garantir que o retorno final seja:
    context = {
        'assunto': assunto,
        'questoes_com_status': questoes_com_status, # Lista COMPLETA
        'filtro': filtro,
        'stats': stats, # Objeto de estatísticas
        'filter': questao_filter,  # Formulário de filtros do django-filter
        'num_questoes': questoes.count()  # Total de questões após filtros
    }
    
    return render(request, 'questoes/listar_questoes.html', context)


# ==============================================================================
# 🟢 NOVAS VIEWS - QUIZ E SIMULADO
# ==============================================================================

@require_POST
@csrf_exempt # Use apenas se a view não estiver autenticada ou for uma API
def validar_resposta_view(request):
    """View que processa a resposta do quiz via AJAX/POST."""
    try:
        # Tenta carregar o JSON do corpo da requisição
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON inválido no corpo da requisição.'}, status=400)
        
        questao_id = data.get('id_questao')      
        alternativa_id = data.get('id_alternativa')
        
        if not questao_id or not alternativa_id:
            return JsonResponse({'success': False, 'error': 'Dados inválidos (ID da Questão ou Alternativa faltando).'}, status=400)
        
        # Busca a questão e alternativa
        questao = get_object_or_404(Questao, id=questao_id)
        alternativa = get_object_or_404(Alternativa, id=alternativa_id)
        
        # VERIFICAÇÃO DE SEGURANÇA: Garante que a alternativa pertence à questão
        if alternativa.id_questao.id != questao.id: 
            return JsonResponse({'success': False, 'error': 'Alternativa não pertence à questão.'}, status=400)
        
        # Verifica se acertou
        acertou = alternativa.eh_correta 
        
        # Salva a resposta do usuário (apenas se estiver logado)
        if request.user.is_authenticated:
            # Apaga respostas anteriores para a mesma questão (se a intenção é salvar apenas a última)
            RespostaUsuario.objects.filter(
                id_usuario=request.user,
                id_questao=questao
            ).delete()
            
            # Cria nova resposta
            RespostaUsuario.objects.create(
                id_usuario=request.user,
                id_questao=questao,
                id_alternativa=alternativa,
                acertou=acertou
            )

        # Busca a alternativa correta (para o feedback visual)
        alternativa_correta = questao.alternativas.filter(eh_correta=True).first()
        
        return JsonResponse({
            'success': True,
            'acertou': acertou,
            'id_alternativa_selecionada': alternativa_id,
            'id_alternativa_correta': alternativa_correta.id if alternativa_correta else None,
            'explicacao': questao.explicacao or '',
        })
        
    except Exception as e:
        error_logger.error(f"Erro inesperado na view validar_resposta_view: {e}", exc_info=True)
        return JsonResponse({'success': False, 'error': 'Erro interno do servidor.'}, status=500)


def quiz_vertical_filtros_view(request, assunto_id):
    """Quiz vertical com filtros dinâmicos - envia todas as questões para o frontend."""
    assunto = get_object_or_404(Assunto, pk=assunto_id)
    
    filtro_ativo = request.GET.get('filtro', 'todas')
    questao_inicial = request.GET.get('questao_inicial', 0)
    
    try:
        questao_inicial = int(questao_inicial)
    except (ValueError, TypeError):
        questao_inicial = 0
    
    user_id = request.user.id if request.user.is_authenticated else None
    questoes_query = Questao.objects.filter(id_assunto=assunto).select_related('id_assunto')
    questoes_com_status = []
    
    respostas_dict = {}
    if user_id:
        # Busca a ÚLTIMA resposta de cada questão do usuário (otimizado)
        questoes_ids_quiz = list(questoes_query.values_list('id', flat=True))
        
        # Primeiro, pega a data máxima de resposta para cada questão
        respostas_agrupadas = RespostaUsuario.objects.filter(
            id_usuario_id=user_id,
            id_questao__in=questoes_ids_quiz
        ).values('id_questao').annotate(
            max_data=Max('data_resposta')
        )
        
        # Monta um dicionário com questão_id -> max_data
        questoes_com_data_maxima = {}
        for item in respostas_agrupadas:
            questoes_com_data_maxima[item['id_questao']] = item['max_data']
        
        # Busca todas as últimas respostas de uma vez (otimizado)
        if questoes_com_data_maxima:
            conditions = Q()
            for questao_id, max_data in questoes_com_data_maxima.items():
                conditions |= Q(id_questao_id=questao_id, data_resposta=max_data)
            
            ultimas_respostas_query = RespostaUsuario.objects.filter(
                id_usuario_id=user_id
            ).filter(conditions).order_by('id_questao_id', '-id')
            
            # Popula o dicionário (pega apenas a primeira resposta de cada questão)
            questoes_processadas = set()
            for resposta in ultimas_respostas_query:
                questao_id = resposta.id_questao.id
                if questao_id not in questoes_processadas:
                    respostas_dict[questao_id] = bool(resposta.acertou)
                    questoes_processadas.add(questao_id)
    
    # Monta lista de questões com status e aplica filtro
    for questao in questoes_query:
        status = 'nao-respondida'
        if questao.id in respostas_dict:
            status = 'certa' if respostas_dict[questao.id] else 'errada'
        
        # Aplicar filtro baseado no filtro_ativo
        incluir_questao = False
        
        if filtro_ativo == 'todas':
            incluir_questao = True
        elif filtro_ativo == 'respondidas':
            incluir_questao = (status == 'certa' or status == 'errada')
        elif filtro_ativo == 'nao-respondidas':
            incluir_questao = (status == 'nao-respondida')
        elif filtro_ativo == 'certas':
            incluir_questao = (status == 'certa')
        elif filtro_ativo == 'erradas':
            incluir_questao = (status == 'errada')
        else:
            incluir_questao = True  # Por padrão, mostra todas
        
        # Adiciona apenas se passar pelo filtro
        if incluir_questao:
            questoes_com_status.append({
                'questao': questao,
                'status': status
            })
    
    # Ordena questões (questão inicial primeiro se especificada)
    if questao_inicial > 0:
        questoes_com_status.sort(key=lambda x: (x['questao'].id != questao_inicial, x['questao'].id))
    else:
        questoes_com_status.sort(key=lambda x: x['questao'].id)
    
    # Busca e associa alternativas
    questoes_ids = [item['questao'].id for item in questoes_com_status]
    alternativas_dict = {}
    
    if questoes_ids:
        alternativas = Alternativa.objects.filter(id_questao__in=questoes_ids).select_related('id_questao').order_by('id_questao', 'ordem', 'id')
        for alt in alternativas:
            if alt.id_questao.id not in alternativas_dict:
                alternativas_dict[alt.id_questao.id] = []
            
            letras = ['A', 'B', 'C', 'D', 'E']
            ordem_index = len(alternativas_dict[alt.id_questao.id])
            letra = letras[ordem_index] if ordem_index < len(letras) else chr(65 + ordem_index)
            
            alternativas_dict[alt.id_questao.id].append({
                'id': alt.id,
                'texto': alt.texto,
                'eh_correta': alt.eh_correta,
                'letra': letra
            })
    
    # Adiciona alternativas às questões e prepara para JSON
    questoes_js = []
    for item in questoes_com_status:
        questao_id = item['questao'].id
        alternativas = alternativas_dict.get(questao_id, [])
        
        questoes_js.append({
            'questao': {
                'id': item['questao'].id,
                'enunciado': item['questao'].texto,
                'texto': item['questao'].texto
            },
            'status': item['status'],
            'alternativas': alternativas
        })
    
    context = {
        'assunto': assunto,
        'questoes': json.dumps(questoes_js),
        'filtro_ativo': filtro_ativo,
        'questao_inicial': questao_inicial,
        'total_questoes': len(questoes_js),
        'user_authenticated': request.user.is_authenticated
    }
    
    return render(request, 'questoes/quiz_vertical_filtros.html', context)
    
def simulado_online_view(request, assunto_id):
    """Simulado online com estrutura similar ao PHP - todas as questões em uma página."""
    # A lógica é quase idêntica a quiz_vertical_filtros_view, mas sem foco na questão inicial
    assunto = get_object_or_404(Assunto, pk=assunto_id)
    filtro_ativo = request.GET.get('filtro', 'todas')
    user_id = request.user.id if request.user.is_authenticated else None
    questoes_query = Questao.objects.filter(id_assunto=assunto).select_related('id_assunto')
    questoes_com_status = []
    
    respostas_dict = {}
    if user_id:
        max_data_subquery = RespostaUsuario.objects.filter(
            id_usuario_id=user_id,
            id_questao=OuterRef('id')
        ).values('id_questao').annotate(
            max_data=Max('data_resposta')
        ).values('max_data')
        
        ultimas_respostas = RespostaUsuario.objects.filter(
            id_usuario_id=user_id,
            id_questao__in=questoes_query.values_list('id', flat=True),
            data_resposta=Subquery(max_data_subquery)
        ).values('id_questao', 'acertou')
        
        for resposta in ultimas_respostas:
            respostas_dict[resposta['id_questao']] = resposta['acertou']
    
    # Monta lista de questões com status (INCLUINDO TODAS)
    for questao in questoes_query:
        status = 'nao-respondida'
        if questao.id in respostas_dict:
            status = 'certa' if respostas_dict[questao.id] else 'errada'
        
        questoes_com_status.append({
            'questao': questao,
            'status': status
        })

    # Busca e associa alternativas
    questoes_ids = [item['questao'].id for item in questoes_com_status]
    alternativas_dict = {}
    
    if questoes_ids:
        alternativas = Alternativa.objects.filter(id_questao__in=questoes_ids).select_related('id_questao').order_by('id_questao', 'ordem', 'id')
        for alt in alternativas:
            if alt.id_questao.id not in alternativas_dict:
                alternativas_dict[alt.id_questao.id] = []
            
            letras = ['A', 'B', 'C', 'D', 'E']
            ordem_index = len(alternativas_dict[alt.id_questao.id])
            letra = letras[ordem_index] if ordem_index < len(letras) else chr(65 + ordem_index)
            
            alternativas_dict[alt.id_questao.id].append({
                'id': alt.id,
                'texto': alt.texto,
                'eh_correta': alt.eh_correta,
                'letra': letra
            })
    
    # Adiciona alternativas às questões
    for item in questoes_com_status:
        item['alternativas'] = alternativas_dict.get(item['questao'].id, [])
    
    # Cálculos de estatísticas para o simulado
    total_questoes = len(questoes_com_status)
    respondidas = len([q for q in questoes_com_status if q['status'] != 'nao-respondida'])
    porcentagem_respondidas = round((respondidas / total_questoes * 100) if total_questoes > 0 else 0, 1)

    context = {
        'assunto': assunto,
        # Passa a lista diretamente para ser renderizada no template
        'questoes_com_status': questoes_com_status,
        'filtro_ativo': filtro_ativo,
        'total_questoes': total_questoes,
        'porcentagem_respondidas': porcentagem_respondidas,
        'user_authenticated': request.user.is_authenticated
    }
    
    return render(request, 'questoes/simulado_online.html', context)


# ===== VIEWS DE AUTENTICAÇÃO E PERFIL =====

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
                    # MELHORIA: Usar o email como username para garantir unicidade.
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


# ==============================================================================
# 🟢 NOVAS VIEWS - RELATÓRIOS (Usuário)
# ==============================================================================

def relatar_problema_view(request):
    """View para o usuário relatar um problema."""
    # A lógica para processar o POST do formulário deve ser adicionada aqui.
    return render(request, 'questoes/relatar_problema.html', {})


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
    
    questao = get_object_or_404(Questao, id=questao_id)
    
    # Por enquanto, apenas redireciona para a página de gerenciamento
    # TODO: Implementar lógica de edição completa
    messages.info(request, f'Edição da questão #{questao_id} será implementada em breve.')
    return redirect('questoes:gerenciar_questoes')


# ==============================================================================
# 🟢 VIEWS - APIs
# ==============================================================================

@csrf_exempt
def api_comentarios(request):
    """Placeholder para a API que lida com comentários."""
    # Lógica da API de comentários (ex: listar, adicionar, curtir)
    return JsonResponse({'status': 'ok', 'data': []}, status=200)

@csrf_exempt
def api_estatisticas(request):
    """Placeholder para a API que lida com estatísticas."""
    # Lógica da API de estatísticas (ex: taxa de acerto por assunto, ranking)
    return JsonResponse({'status': 'ok', 'data': {}}, status=200)

@csrf_exempt
def api_notificacoes(request):
    """Placeholder para a API de notificações."""
    # Lógica da API de notificações (ex: notificações do admin)
    return JsonResponse({'status': 'ok', 'notifications': []}, status=200)