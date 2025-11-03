from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q, Sum, Avg, Case, When, IntegerField, FloatField, F, ExpressionWrapper, Max, OuterRef, Subquery
from django.utils import timezone
from django.core.paginator import Paginator
from django.conf import settings
from datetime import timedelta, datetime
from collections import Counter
import json
import logging
import traceback
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
# Importar views de gerenciamento de comentários e assuntos do views_container
from .views_container import (
    gerenciar_comentarios_view,
    toggle_comentario_view,
    deletar_comentario_view,
    adicionar_assunto_view,
    gerenciar_assuntos_view,
    deletar_assunto_view
)

error_logger = logging.getLogger('questoes.errors')

# ---
## ===== VIEWS PÚBLICAS =====

def index_view(request):
    """View da página inicial do sistema"""
    from datetime import datetime, timedelta
    
    total_assuntos = Assunto.objects.count()
    total_questoes = Questao.objects.count()
    total_alternativas = Alternativa.objects.count()
    
    # Cálculo da semana atual (Domingo à meia-noite até Sábado 23:59:59)
    hoje = timezone.now().date()
    # weekday() retorna: 0=Segunda, 1=Terça, ..., 6=Domingo
    # Ajustar para semana começar no domingo (0=Domingo, 1=Segunda, ..., 6=Sábado)
    dia_semana_atual = hoje.weekday()  # 0=Seg, 1=Ter, ..., 6=Dom
    # Converte para: 0=Domingo, 1=Segunda, ..., 6=Sábado
    if dia_semana_atual == 6:  # Se é domingo
        dias_desde_domingo = 0
    else:  # Se é segunda a sábado
        dias_desde_domingo = dia_semana_atual + 1  # +1 porque domingo é o dia 0
    
    inicio_semana = hoje - timedelta(days=dias_desde_domingo)
    fim_semana = inicio_semana + timedelta(days=7)
    
    # Converter para datetime para comparar com data_resposta (DateTimeField)
    # Início: Domingo à meia-noite (00:00:00)
    inicio_semana_dt = timezone.make_aware(datetime.combine(inicio_semana, datetime.min.time()))
    # Fim: Próximo domingo à meia-noite (00:00:00) - isso garante que sábado 23:59:59 ainda está incluído
    fim_semana_dt = timezone.make_aware(datetime.combine(fim_semana, datetime.min.time()))
    
    # Query para Top 5 ranking semanal
    ranking_query = RespostaUsuario.objects.filter(
        data_resposta__gte=inicio_semana_dt,
        data_resposta__lt=fim_semana_dt,
        id_usuario__isnull=False
    ).values('id_usuario').annotate(
        total=Count('id'),
        acertos=Count('id', filter=Q(acertou=True))
    ).order_by('-total', '-acertos')[:5]
    
    ranking_semanal = []
    for item in ranking_query:
        if item['id_usuario']:
            try:
                usuario = User.objects.get(pk=item['id_usuario'])
                taxa_acerto = round((item['acertos'] / item['total']) * 100) if item['total'] > 0 else 0
                ranking_semanal.append({
                    'id_usuario': usuario.id,
                    'nome': usuario.first_name or usuario.username,
                    'username': usuario.username,
                    'total': item['total'],
                    'acertos': item['acertos'],
                    'taxa_acerto': taxa_acerto
                })
            except User.DoesNotExist:
                continue
    
    # Calcular posição do usuário atual (se logado e não estiver no Top 5)
    posicao_usuario = None
    dados_usuario = None
    
    if request.user.is_authenticated:
        # Verifica se usuário está no Top 5
        usuario_no_top5 = any(item['id_usuario'] == request.user.id for item in ranking_semanal)
        
        if not usuario_no_top5:
            # Buscar dados do usuário na semana atual
            dados_usuario_semana = RespostaUsuario.objects.filter(
                data_resposta__gte=inicio_semana_dt,
                data_resposta__lt=fim_semana_dt,
                id_usuario=request.user
            ).aggregate(
                total=Count('id'),
                acertos=Count('id', filter=Q(acertou=True))
            )
            
            # Se o usuário tem dados da semana, calcular posição
            if dados_usuario_semana['total'] and dados_usuario_semana['total'] > 0:
                # Buscar todos os dados para calcular posição completa
                todos_rankings = RespostaUsuario.objects.filter(
                    data_resposta__gte=inicio_semana_dt,
                    data_resposta__lt=fim_semana_dt,
                    id_usuario__isnull=False
                ).values('id_usuario').annotate(
                    total=Count('id'),
                    acertos=Count('id', filter=Q(acertou=True))
                ).order_by('-total', '-acertos')
                
                # Encontrar posição do usuário
                for idx, item in enumerate(todos_rankings, start=1):
                    if item['id_usuario'] == request.user.id:
                        taxa_acerto = round((item['acertos'] / item['total']) * 100) if item['total'] > 0 else 0
                        posicao_usuario = idx
                        dados_usuario = {
                            'id_usuario': request.user.id,
                            'nome': request.user.first_name or request.user.username,
                            'username': request.user.username,
                            'total': item['total'],
                            'acertos': item['acertos'],
                            'taxa_acerto': taxa_acerto,
                            'posicao': idx
                        }
                        break
    
    # Calcular max_total para barras de progresso
    if ranking_semanal:
        max_total = ranking_semanal[0]['total']
        if max_total == 0:
            max_total = 1
    else:
        # Se não há ranking mas há dados do usuário, usa o total do usuário
        max_total = dados_usuario['total'] if dados_usuario and dados_usuario.get('total', 0) > 0 else 1
    
    notificacoes = []
    if request.user.is_authenticated:
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
        'max_total': max_total,
        'posicao_usuario': posicao_usuario,
        'dados_usuario': dados_usuario,
        'inicio_semana': inicio_semana,  # Domingo da semana
        'fim_semana': fim_semana - timedelta(days=1),  # Sábado da semana
        'notificacoes': notificacoes,
        'is_admin': is_admin,
        'user': request.user
    }
    
    return render(request, 'questoes/index.html', context)

# ---
## ===== VIEWS DE QUIZ/QUESTÕES =====

def estatisticas_questao(request, questao_id):
    """
    Estatísticas de uma questão específica:
    - Contagem de respostas por alternativa
    - Taxa de acerto geral
    """
    questao = get_object_or_404(Questao, pk=questao_id)

    # Mapeia alternativas (ordem -> letra)
    alternativas = list(Alternativa.objects.filter(id_questao=questao).order_by('ordem', 'id'))
    letras = ['A', 'B', 'C', 'D', 'E']
    alt_id_para_label = {}
    for idx, alt in enumerate(alternativas):
        letra = letras[idx] if idx < len(letras) else chr(65 + idx)
        alt_id_para_label[alt.id] = f"Alternativa {letra}"

    # Parâmetros
    scope = request.GET.get('scope', 'user')
    try:
        days = int(request.GET.get('days', '14'))
    except ValueError:
        days = 14
    days = max(1, min(days, 90))

    base_qs = RespostaUsuario.objects.filter(id_questao=questao)
    if scope == 'user' and request.user.is_authenticated:
        base_qs = base_qs.filter(id_usuario=request.user)
    
    # Para histórico, buscar TODAS as respostas do usuário (sem filtro de data)
    base_qs_historico = RespostaUsuario.objects.filter(id_questao=questao)
    if scope == 'user' and request.user.is_authenticated:
        base_qs_historico = base_qs_historico.filter(id_usuario=request.user)

    # Contagem por alternativa selecionada
    contagem_respostas = (
        base_qs
        .values('id_alternativa')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    labels, data = [], []
    for item in contagem_respostas:
        alt_id = item.get('id_alternativa')
        labels.append(alt_id_para_label.get(alt_id, 'Alternativa'))
        data.append(item.get('total', 0))

    # Para estatísticas do usuário, usar histórico completo; para gerais, usar período configurado
    if scope == 'user' and request.user.is_authenticated:
        # Usar histórico completo para totais quando for estatísticas do usuário
        total_respostas = base_qs_historico.count()
        total_acertos = base_qs_historico.filter(acertou=True).count()
    else:
        # Usar período configurado para estatísticas gerais
        total_respostas = base_qs.count()
        total_acertos = base_qs.filter(acertou=True).count()
    
    percentual_acerto = round((total_acertos / total_respostas) * 100, 2) if total_respostas > 0 else 0

    # Timeline diária dos últimos N dias
    from datetime import date, timedelta
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    # Agrupa por dia
    timeline_qs = (
        base_qs
        .filter(data_resposta__date__gte=start_date)
        .values('data_resposta__date')
        .annotate(qty=Count('id'))
        .order_by('data_resposta__date')
    )
    # Preenche zeros
    labels_tl = []
    counts_tl = []
    idx = {}
    cur = start_date
    while cur <= end_date:
        labels_tl.append(cur.isoformat())
        counts_tl.append(0)
        idx[cur] = len(counts_tl)-1
        cur += timedelta(days=1)
    for row in timeline_qs:
        d = row['data_resposta__date']
        if d in idx:
            counts_tl[idx[d]] = row['qty']

    # Se requisitado como JSON (para render inline via AJAX ou modal)
    if request.GET.get('format') == 'json' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        assunto_nome = getattr(questao.id_assunto, 'nome', '')
        by_alt = { 'A':0,'B':0,'C':0,'D':0,'E':0 }
        # Map id_alternativa -> letra usando ordem
        alt_id_to_letter = {}
        for idxa, alt in enumerate(alternativas):
            letra = letras[idxa] if idxa < len(letras) else chr(65+idxa)
            alt_id_to_letter[alt.id] = letra
        
        # Contagem de TODAS as respostas (incluindo histórico completo se for scope='user')
        # Usar base_qs_historico para contar todas as respostas do usuário
        if scope == 'user' and request.user.is_authenticated:
            # Para estatísticas do usuário, contar TODAS as respostas (sem limite de período)
            contagem_respostas_completa = (
                base_qs_historico
                .values('id_alternativa')
                .annotate(total=Count('id'))
                .order_by('-total')
            )
        else:
            # Para estatísticas gerais, usar base_qs (com período configurado)
            contagem_respostas_completa = contagem_respostas
        
        for item in contagem_respostas_completa:
            letra = alt_id_to_letter.get(item['id_alternativa'])
            if letra:
                by_alt[letra] = int(item['total'])
        
        # Histórico de respostas individuais (apenas para scope='user')
        historico = []
        try:
            if scope == 'user' and request.user.is_authenticated:
                from django.utils import timezone
                # Buscar pelo menos as últimas 20 respostas (sem limite de data)
                # Usar base_qs_historico que não tem filtro de período
                historico_respostas = base_qs_historico.order_by('-data_resposta')[:20]  # Últimas 20
                
                # Log para debug
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f'Histórico: buscando respostas para questão {questao.id}, usuário {request.user.id}')
                
                # Converter para lista para garantir que podemos contar
                historico_lista = list(historico_respostas)
                logger.info(f'Histórico: total de respostas encontradas: {len(historico_lista)}')
                
                for resposta in historico_lista:
                    letra_escolhida = alt_id_to_letter.get(resposta.id_alternativa_id, '?')
                    data_formatada = timezone.localtime(resposta.data_resposta).strftime('%d/%m/%Y')
                    historico.append({
                        'data': data_formatada,
                        'data_iso': resposta.data_resposta.isoformat(),
                        'alternativa': letra_escolhida,
                        'acertou': resposta.acertou,
                    })
                
                logger.info(f'Histórico: {len(historico)} itens processados para retorno')
        except Exception as e:
            # Se houver erro ao buscar histórico, apenas não incluir histórico (não quebrar a resposta)
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Erro ao buscar histórico: {e}', exc_info=True)
            historico = []
        
        return JsonResponse({
            'success': True,
            'data': {
                'id_questao': questao.id,
                'assunto': assunto_nome,
                'scope': 'user' if (scope=='user' and request.user.is_authenticated) else 'global',
                'period_days': days,
                'totals': {
                    'total_attempts': total_respostas,
                    'correct_attempts': total_acertos,
                    'wrong_attempts': max(0, total_respostas-total_acertos),
                    'accuracy_percent': percentual_acerto,
                },
                'by_alternative': by_alt,
                'timeline': { 'labels': labels_tl, 'counts': counts_tl },
                'historico': historico,  # Histórico individual de respostas
            }
        })

    context = {
        'questao': questao,
        'labels_json': json.dumps(labels),
        'data_json': json.dumps(data),
        'total_respostas': total_respostas,
        'percentual_acerto': percentual_acerto,
    }

    return render(request, 'questoes/estatisticas_detalhe.html', context)

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
        'total_assuntos': assuntos.count(),
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
    from django.db import IntegrityError
    try:
        # Tenta carregar o JSON do corpo da requisição
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON inválido no corpo da requisição.'}, status=400)
        
        questao_id = int(data.get('id_questao')) if data.get('id_questao') is not None else None
        alternativa_id = int(data.get('id_alternativa')) if data.get('id_alternativa') is not None else None
        
        if not questao_id or not alternativa_id:
            return JsonResponse({'success': False, 'error': 'Dados inválidos (ID da Questão ou Alternativa faltando).'}, status=400)
        
        # Busca a questão e alternativa
        questao = get_object_or_404(Questao, id=questao_id)
        alternativa = get_object_or_404(Alternativa, id=alternativa_id)
        
        # VERIFICAÇÃO DE SEGURANÇA: Garante que a alternativa pertence à questão
        if alternativa.id_questao.id != questao.id: 
            return JsonResponse({'success': False, 'error': 'Alternativa não pertence à questão.'}, status=400)
        
        # --- NOVA LÓGICA DE VALIDAÇÃO ---
        # Fonte de verdade do acerto: a própria alternativa clicada
        alternativas_queryset = questao.alternativas.all()
        acertou = bool(alternativa.eh_correta)
        # Obter alternativa correta apenas para retornar ID ao frontend
        alternativa_correta = alternativas_queryset.filter(eh_correta=True).first()
        
        # Salva a resposta do usuário (apenas se estiver logado)
        if request.user.is_authenticated:
            # NÃO apagar respostas anteriores - manter histórico de todas as respostas
            # Cria nova resposta (mantendo histórico completo)
            try:
                RespostaUsuario.objects.create(
                    id_usuario=request.user,
                    id_questao=questao,
                    id_alternativa=alternativa,
                    acertou=acertou
                )
            except IntegrityError as e:
                # Se houver erro de constraint (unique_together ainda existe no banco),
                # tenta atualizar a resposta existente em vez de criar nova
                try:
                    # Atualiza a resposta existente (mantém apenas a última)
                    RespostaUsuario.objects.filter(
                        id_usuario=request.user,
                        id_questao=questao
                    ).update(
                        id_alternativa=alternativa,
                        acertou=acertou,
                        data_resposta=timezone.now()
                    )
                except Exception as update_err:
                    # Se mesmo atualizar der erro, apenas loga e continua
                    error_logger.warning(f'Erro ao atualizar resposta após IntegrityError: {update_err}')
            except Exception as e:
                # Outro tipo de erro - logar mas continuar (não quebrar o fluxo)
                error_logger.error(f'Erro ao salvar resposta (não IntegrityError): {e}', exc_info=True)
                # Não quebrar o fluxo se houver erro ao salvar - continua para retornar resposta ao frontend

        # alternativa_correta já obtida acima
        
        # Sempre retornar sucesso, mesmo se houver erro ao salvar no banco
        # (o erro já foi tratado acima e logado)
        return JsonResponse({
            'success': True,
            'acertou': acertou,
            'id_alternativa_selecionada': alternativa_id,
            'id_alternativa_correta': alternativa_correta.id if alternativa_correta else None,
            'explicacao': questao.explicacao or '',
            # campos de diagnóstico temporários
            'debug': {
                'questao_id': questao.id,
                'selecionada_eh_correta': bool(alternativa.eh_correta),
                'alternativas': [
                    {
                        'id': alt.id,
                        'eh_correta': bool(alt.eh_correta)
                    } for alt in alternativas_queryset
                ]
            }
        })
        
    except Exception as e:
        error_logger.error(f"Erro inesperado na view validar_resposta_view: {e}", exc_info=True)
        # Retornar erro detalhado para debug (remover em produção se necessário)
        import traceback
        error_details = {
            'success': False, 
            'error': 'Erro interno do servidor.',
            'debug_message': str(e) if hasattr(e, '__str__') else 'Erro desconhecido'
        }
        if settings.DEBUG:
            error_details['traceback'] = traceback.format_exc()
        return JsonResponse(error_details, status=500)


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
    
    # Adiciona alternativas às questões: lista Python para render HTML e JSON para JS
    questoes_para_renderizar = []
    questoes_js = []
    for item in questoes_com_status:
        questao_id = item['questao'].id
        alternativas = alternativas_dict.get(questao_id, [])

        # lista Python para o template (inclui alternativas)
        questoes_para_renderizar.append({
            'questao': item['questao'],
            'status': item['status'],
            'alternativas': alternativas,
        })

        # versão serializada para JS
        questoes_js.append({
            'questao': {
                'id': item['questao'].id,
                'enunciado': item['questao'].texto,
                'texto': item['questao'].texto,
            },
            'status': item['status'],
            'alternativas': alternativas,
        })
    
    context = {
        'assunto': assunto,
        # json_script espera um objeto Python serializável, NÃO string JSON
        'questoes_json_seguro': questoes_js,
        'questoes_para_renderizar': questoes_para_renderizar,
        'filtro_ativo': filtro_ativo,
        'questao_inicial': questao_inicial,
        'total_questoes': len(questoes_js),
        'user_authenticated': request.user.is_authenticated,
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
        return redirect('questoes:index')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        user_type = request.POST.get('user_type', 'usuario')
        
        if not email or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
        elif not user_type:
            messages.error(request, 'Por favor, selecione o tipo de usuário.')
        else:
            try:
                # Tenta encontrar o usuário pelo email
                user = User.objects.get(email=email)
                
                # Validação: Se selecionou "admin", o usuário DEVE ser admin
                if user_type == 'admin' and not user.is_staff:
                    messages.error(request, 'Você não tem permissão de administrador. Use o botão "Usuário Normal" para fazer login.')
                    return render(request, 'questoes/login.html')
                
                # CORREÇÃO/MELHORIA: Autenticar usando o username encontrado.
                user_auth = authenticate(request, username=user.username, password=password)
                
                if user_auth is not None:
                    login(request, user_auth)
                    messages.success(request, f'Bem-vindo(a), {user.first_name or user.username}!')
                    return redirect('questoes:index')
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
        return redirect('questoes:index')
    
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
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard_view(request):
    """Dashboard administrativo com métricas e estatísticas"""
    
    total_usuarios = User.objects.count()
    total_respostas = RespostaUsuario.objects.count()
    
    hoje = timezone.now().date()
    hoje_inicio = timezone.make_aware(datetime.combine(hoje, datetime.min.time()))
    
    # Logins hoje (usuários que fizeram login hoje)
    usuarios_hoje = User.objects.filter(last_login__gte=hoje_inicio).count() if User.objects.filter(last_login__isnull=False).exists() else 0
    
    # Logins última semana
    semana_inicio = hoje_inicio - timedelta(days=7)
    usuarios_semana = User.objects.filter(last_login__gte=semana_inicio).count() if User.objects.filter(last_login__isnull=False).exists() else 0
    
    # Logins último mês
    mes_inicio = hoje_inicio - timedelta(days=30)
    usuarios_mes = User.objects.filter(last_login__gte=mes_inicio).count() if User.objects.filter(last_login__isnull=False).exists() else 0
    
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


@login_required
@user_passes_test(lambda u: u.is_staff)
def gerenciar_assuntos_view(request):
    """View para gerenciar assuntos/conteúdos"""
    
    assuntos = Assunto.objects.annotate(
        total_questoes=Count('questoes')
    ).order_by('-criado_em')
    
    total_assuntos = Assunto.objects.count()
    total_questoes = Questao.objects.count()
    
    context = {
        'assuntos': assuntos,
        'total_assuntos': total_assuntos,
        'total_questoes': total_questoes,
    }
    
    return render(request, 'questoes/gerenciar_assuntos.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def deletar_assunto_view(request):
    """Deleta um assunto (apenas para staff/admin)"""
    if request.method != 'POST':
        messages.error(request, 'Método não permitido.')
        return redirect('questoes:gerenciar_assuntos')
    
    assunto_id = request.POST.get('assunto_id')
    if not assunto_id:
        messages.error(request, 'ID do assunto não fornecido.')
        return redirect('questoes:gerenciar_assuntos')
    
    try:
        assunto = Assunto.objects.get(id=assunto_id)
        
        # Verificar se o assunto tem questões
        total_questoes = assunto.questoes.count()
        if total_questoes > 0:
            messages.error(request, f'Não é possível excluir o conteúdo "{assunto.nome}" pois ele possui {total_questoes} questão(ões) associada(s).')
            return redirect('questoes:gerenciar_assuntos')
        
        nome_assunto = assunto.nome
        assunto.delete()
        messages.success(request, f'Conteúdo "{nome_assunto}" excluído com sucesso!')
    except Assunto.DoesNotExist:
        messages.error(request, f'Conteúdo #{assunto_id} não encontrado.')
    except Exception as e:
        error_logger.error(f'Erro ao deletar assunto {assunto_id}: {e}', exc_info=True)
        messages.error(request, f'Erro ao excluir conteúdo: {str(e)}')
    
    return redirect('questoes:gerenciar_assuntos')


def admin_login_view(request):
    """Login para administradores"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('questoes:index')
    
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
                    return redirect('questoes:index')
                else:
                    messages.error(request, 'Email ou senha incorretos, ou você não tem permissão de administrador.')
            except User.DoesNotExist:
                messages.error(request, 'Email ou senha incorretos, ou você não tem permissão de administrador.')
    
    return render(request, 'questoes/admin_login.html') 
# ===== VIEWS ADMIN - GERENCIAMENTO =====
@login_required
@user_passes_test(lambda u: u.is_staff)
def gerenciar_questoes_view(request):
    """Exibe a lista de questões para gerenciamento admin"""
    
    # Agrupar questões por assunto
    assuntos_com_questoes = Assunto.objects.annotate(
        total_questoes_assunto=Count('questoes')
    ).filter(total_questoes_assunto__gt=0).order_by('tipo_assunto', 'nome')
    
    # Criar dicionário agrupado: {assunto: [questoes]}
    questoes_agrupadas = {}
    for assunto in assuntos_com_questoes:
        questoes_do_assunto = Questao.objects.filter(
            id_assunto=assunto
        ).select_related('id_assunto').annotate(
        total_alternativas=Count('alternativas')
        ).order_by('id')  # Ordenar por ID dentro de cada assunto
        questoes_agrupadas[assunto] = list(questoes_do_assunto)
    
    # Total geral de questões
    total_questoes = Questao.objects.count()
    
    context = {
        'questoes_agrupadas': questoes_agrupadas,
        'total_questoes': total_questoes,
    }
    
    return render(request, 'questoes/gerenciar_questoes.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def deletar_questao_view(request):
    """Deleta uma questão (apenas para staff/admin)"""
    if request.method != 'POST':
        messages.error(request, 'Método não permitido.')
        return redirect('questoes:gerenciar_questoes')
    
    questao_id = request.POST.get('questao_id')
    if not questao_id:
        messages.error(request, 'ID da questão não fornecido.')
        return redirect('questoes:gerenciar_questoes')
    
    try:
        questao = Questao.objects.get(id=questao_id)
        questao.delete()
        messages.success(request, f'Questão #{questao_id} deletada com sucesso!')
    except Questao.DoesNotExist:
        messages.error(request, f'Questão #{questao_id} não encontrada.')
    except Exception as e:
        messages.error(request, f'Erro ao deletar questão: {str(e)}')
    
    return redirect('questoes:gerenciar_questoes')


@login_required
@user_passes_test(lambda u: u.is_staff)
@require_POST
def deletar_todas_questoes_assunto_view(request):
    """Deleta todas as questões de um assunto específico (apenas para staff/admin)"""
    assunto_id = request.POST.get('assunto_id')
    
    if not assunto_id:
        messages.error(request, 'ID do assunto não fornecido.')
        return redirect('questoes:gerenciar_questoes')
    
    try:
        assunto = Assunto.objects.get(id=assunto_id)
        questoes_count = Questao.objects.filter(id_assunto=assunto).count()
        
        if questoes_count == 0:
            messages.warning(request, f'O assunto "{assunto.nome}" não possui questões para deletar.')
            return redirect('questoes:gerenciar_questoes')
        
        # Usar transação para garantir integridade
        with transaction.atomic():
            # Deleta todas as questões do assunto (isso também deleta as alternativas via CASCADE)
            questoes_deletadas = Questao.objects.filter(id_assunto=assunto).delete()
            count = questoes_deletadas[0]  # Número de objetos deletados
        
        messages.success(request, f'✅ {count} questão(ões) do assunto "{assunto.nome}" foram deletadas com sucesso!')
        
    except Assunto.DoesNotExist:
        messages.error(request, f'Assunto com ID {assunto_id} não encontrado.')
    except Exception as e:
        error_logger.error(f'Erro ao deletar questões do assunto: {e}', exc_info=True)
        messages.error(request, f'Erro ao deletar questões: {str(e)}')
    
    return redirect('questoes:gerenciar_questoes')


@login_required
@user_passes_test(lambda u: u.is_staff)
def adicionar_questao_view(request):
    """View para adicionar nova questão com seletores encadeados"""
    
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
@user_passes_test(lambda u: u.is_staff)
def editar_questao_view(request, questao_id):
    """Edita uma questão existente"""
    
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
    """API para listar comentários de uma questão com ordenação"""
    try:
        if request.method != 'GET':
            return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)
        
        questao_id = request.GET.get('questao_id')
        ordenacao = request.GET.get('ordenacao', 'data')  # 'data' ou 'curtidas'
        
        error_logger.info(f'[api_comentarios] Requisição recebida: questao_id={questao_id} (tipo: {type(questao_id).__name__}), ordenacao={ordenacao}')
        
        if not questao_id:
            return JsonResponse({'success': False, 'message': 'ID da questão não fornecido'}, status=400)
        
        # Converter para int se necessário
        try:
            questao_id_int = int(questao_id)
        except (ValueError, TypeError):
            error_logger.error(f'[api_comentarios] ID inválido: {questao_id}')
            return JsonResponse({'success': False, 'message': 'ID da questão inválido'}, status=400)
        
        try:
            questao = Questao.objects.get(id=questao_id_int)
            error_logger.info(f'[api_comentarios] Questão encontrada: ID={questao.id}, Nome={questao.texto[:50]}...')
        except Questao.DoesNotExist:
            error_logger.error(f'[api_comentarios] Questão não encontrada: ID={questao_id_int}')
            return JsonResponse({'success': False, 'message': 'Questão não encontrada'}, status=404)
        
        # Verificar TODOS os comentários desta questão (sem filtros) - PARA DEBUG
        todos_comentarios_debug = ComentarioQuestao.objects.filter(id_questao=questao_id_int)
        error_logger.info(f'[api_comentarios] Total de comentários na questão {questao_id_int} (sem filtros): {todos_comentarios_debug.count()}')
        for c in todos_comentarios_debug[:10]:  # Limitar a 10 para não encher o log
            error_logger.info(f'  - Comentário ID {c.id}: ativo={c.ativo}, aprovado={c.aprovado}, pai={c.id_comentario_pai_id}')
        
        # Buscar comentários principais (sem pai)
        # IMPORTANTE: Comentários são públicos, visíveis para TODOS os usuários
        # Usar questao_id_int para garantir consistência (testado e funcionando)
        comentarios_qs = ComentarioQuestao.objects.filter(
            id_questao=questao_id_int,
            id_comentario_pai__isnull=True,
            ativo=True,
            aprovado=True
        )
        
        # Log para debug - ANTES da ordenação
        total_comentarios_antes = comentarios_qs.count()
        error_logger.info(f'[api_comentarios] Questão ID: {questao_id_int}, Total de comentários encontrados (antes ordenação): {total_comentarios_antes}')
        
        # Log ANTES da ordenação
        error_logger.info(f'[api_comentarios] QuerySet antes ordenação: {comentarios_qs.count()} comentários')
        
        # Ordenação
        if ordenacao == 'curtidas':
            # Annotate com total de curtidas e ordenar
            try:
                # Usar Count com related_name 'curtidas' e filtrar por ativo=True
                # Remover distinct=True pois pode causar problemas
                comentarios_qs = comentarios_qs.annotate(
                    total_curtidas=Count('curtidas', filter=Q(curtidas__ativo=True))
                ).order_by('-total_curtidas', '-data_comentario')
                error_logger.info(f'[api_comentarios] Ordenação por curtidas aplicada: {comentarios_qs.count()} comentários')
            except Exception as e:
                error_logger.error(f'Erro ao ordenar por curtidas: {str(e)}', exc_info=True)
                error_logger.error(f'Traceback: {traceback.format_exc()}')
                # Fallback para ordenação por data
                comentarios_qs = comentarios_qs.order_by('-data_comentario')
        else:
            # Ordenar por data (padrão)
            comentarios_qs = comentarios_qs.order_by('-data_comentario')
            error_logger.info(f'[api_comentarios] Ordenação por data aplicada: {comentarios_qs.count()} comentários')
        
        # Log DEPOIS da ordenação e ANTES do loop
        error_logger.info(f'[api_comentarios] QuerySet depois ordenação (antes loop): {comentarios_qs.count()} comentários')
        
        # Converter QuerySet para lista para garantir que seja avaliado
        comentarios_lista = list(comentarios_qs)
        error_logger.info(f'[api_comentarios] Total de comentários convertidos para lista: {len(comentarios_lista)}')
        
        comentarios_data = []
        for idx, comentario in enumerate(comentarios_lista):
            error_logger.info(f'[api_comentarios] Processando comentário {idx+1}/{len(comentarios_lista)}: ID={comentario.id}')
            try:
                # Contar curtidas
                total_curtidas = comentario.curtidas.filter(ativo=True).count() if hasattr(comentario, 'curtidas') else 0
                
                # Verificar se usuário atual curtiu
                curtido_pelo_usuario = False
                if request.user.is_authenticated and hasattr(comentario, 'curtidas'):
                    try:
                        curtido_pelo_usuario = comentario.curtidas.filter(
                            id_usuario=request.user,
                            ativo=True
                        ).exists()
                    except Exception as e:
                        error_logger.error(f'Erro ao verificar curtida do usuário: {str(e)}')
                
                # Contar respostas
                total_respostas = 0
                respostas = []
                if hasattr(comentario, 'respostas'):
                    try:
                        total_respostas = comentario.respostas.filter(
                            ativo=True,
                            aprovado=True
                        ).count()
                        
                        # Buscar respostas
                        respostas = comentario.respostas.filter(ativo=True, aprovado=True).order_by('-data_comentario')[:5]
                    except Exception as e:
                        error_logger.error(f'Erro ao buscar respostas: {str(e)}')
                
                # Buscar respostas
                respostas_data = []
                for resposta in respostas:
                    try:
                        resp_curtidas = resposta.curtidas.filter(ativo=True).count() if hasattr(resposta, 'curtidas') else 0
                        resp_curtido_pelo_usuario = False
                        if request.user.is_authenticated and hasattr(resposta, 'curtidas'):
                            try:
                                resp_curtido_pelo_usuario = resposta.curtidas.filter(
                                    id_usuario=request.user,
                                    ativo=True
                                ).exists()
                            except Exception:
                                pass
                        
                        respostas_data.append({
                            'id_comentario': resposta.id,
                            'id': resposta.id,  # Fallback
                            'nome_usuario': resposta.nome_usuario or 'Usuário',
                            'comentario': resposta.comentario,
                            'data_formatada': resposta.data_comentario.strftime('%d/%m/%Y às %H:%M') if resposta.data_comentario else '',
                            'total_curtidas': resp_curtidas,
                            'curtido_pelo_usuario': resp_curtido_pelo_usuario,
                        })
                    except Exception as e:
                        error_logger.error(f'Erro ao processar resposta: {str(e)}')
                        continue
                
                comentarios_data.append({
                    'id_comentario': comentario.id,
                    'id': comentario.id,  # Fallback
                    'nome_usuario': comentario.nome_usuario or 'Usuário',
                    'comentario': comentario.comentario,
                    'data_formatada': comentario.data_comentario.strftime('%d/%m/%Y às %H:%M') if comentario.data_comentario else '',
                    'total_curtidas': total_curtidas,
                    'curtido_pelo_usuario': curtido_pelo_usuario,
                    'total_respostas': total_respostas,
                    'respostas': respostas_data,
                })
            except Exception as e:
                error_logger.error(f'Erro ao processar comentário {comentario.id if hasattr(comentario, "id") else "desconhecido"}: {str(e)}')
                continue
        
        error_logger.info(f'[api_comentarios] Total de comentários adicionados ao array de retorno: {len(comentarios_data)}')
        
        return JsonResponse({
            'success': True,
            'data': comentarios_data
        }, status=200)
    
    except Exception as e:
        error_logger.error(f'Erro geral em api_comentarios: {str(e)}', exc_info=True)
        error_logger.error(f'Traceback: {traceback.format_exc()}')
        return JsonResponse({
            'success': False,
            'message': f'Erro ao carregar comentários: {str(e)}'
        }, status=500)

@csrf_exempt
@login_required
def api_criar_comentario(request):
    """API para criar um novo comentário"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)
    
    try:
        questao_id = request.POST.get('questao_id')
        comentario_texto = request.POST.get('comentario', '').strip()
        comentario_pai_id = request.POST.get('comentario_pai_id', None)  # Opcional - para respostas
        
        if not questao_id:
            return JsonResponse({'success': False, 'message': 'ID da questão não fornecido'}, status=400)
        
        # Converter para int se necessário
        try:
            questao_id_int = int(questao_id)
        except (ValueError, TypeError):
            error_logger.error(f'[api_criar_comentario] ID inválido: {questao_id}')
            return JsonResponse({'success': False, 'message': 'ID da questão inválido'}, status=400)
        
        # Validar comentário pai se fornecido (para respostas)
        comentario_pai = None
        if comentario_pai_id:
            try:
                comentario_pai_id_int = int(comentario_pai_id)
                comentario_pai = ComentarioQuestao.objects.get(id=comentario_pai_id_int)
                # Validar que o comentário pai pertence à mesma questão
                if comentario_pai.id_questao_id != questao_id_int:
                    return JsonResponse({'success': False, 'message': 'Comentário pai não pertence à questão especificada'}, status=400)
            except (ValueError, TypeError):
                return JsonResponse({'success': False, 'message': 'ID do comentário pai inválido'}, status=400)
            except ComentarioQuestao.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Comentário pai não encontrado'}, status=404)
        
        if not comentario_texto:
            return JsonResponse({'success': False, 'message': 'Comentário não pode estar vazio'}, status=400)
        
        if len(comentario_texto) < 10:
            return JsonResponse({'success': False, 'message': 'Comentário deve ter pelo menos 10 caracteres'}, status=400)
        
        if len(comentario_texto) > 500:
            return JsonResponse({'success': False, 'message': 'Comentário não pode ter mais de 500 caracteres'}, status=400)
        
        try:
            questao = Questao.objects.get(id=questao_id_int)
        except Questao.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Questão não encontrada'}, status=404)
        
        # Criar comentário (principal ou resposta)
        novo_comentario = ComentarioQuestao.objects.create(
            id_questao=questao,
            nome_usuario=request.user.first_name or request.user.username,
            email_usuario=request.user.email if request.user.email else None,
            id_usuario=request.user,
            comentario=comentario_texto,
            id_comentario_pai=comentario_pai,  # Será None para comentários principais
            ativo=True,
            aprovado=True
        )
        
        # Forçar refresh do objeto do banco para garantir que está salvo
        novo_comentario.refresh_from_db()
        
        tipo_comentario = 'resposta' if comentario_pai else 'comentário principal'
        error_logger.info(f'[api_criar_comentario] {tipo_comentario.capitalize()} criado: ID={novo_comentario.id}, Questão={questao_id_int}, Pai={comentario_pai.id if comentario_pai else None}, Ativo={novo_comentario.ativo}, Aprovado={novo_comentario.aprovado}')
        
        return JsonResponse({
            'success': True,
            'message': f'{tipo_comentario.capitalize()} adicionado com sucesso!',
            'comentario_id': novo_comentario.id,
            'is_resposta': comentario_pai is not None,
            'comentario_pai_id': comentario_pai.id if comentario_pai else None
        }, status=200)
        
    except Exception as e:
        error_logger.error(f'Erro ao criar comentário: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Erro ao criar comentário: {str(e)}'
        }, status=500)

@csrf_exempt
@login_required
def api_curtir_comentario(request):
    """API para curtir/descurtir um comentário"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)
    
    try:
        comentario_id = request.POST.get('comentario_id')
        
        if not comentario_id:
            return JsonResponse({'success': False, 'message': 'ID do comentário não fornecido'}, status=400)
        
        try:
            comentario_id_int = int(comentario_id)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'message': 'ID do comentário inválido'}, status=400)
        
        try:
            comentario = ComentarioQuestao.objects.get(id=comentario_id_int)
        except ComentarioQuestao.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Comentário não encontrado'}, status=404)
        
        # Verificar se usuário já curtiu
        curtida_existente = CurtidaComentario.objects.filter(
            id_comentario=comentario,
            id_usuario=request.user,
            ativo=True
        ).first()
        
        if curtida_existente:
            # Descurtir - marcar como inativo
            curtida_existente.ativo = False
            curtida_existente.save()
            curtido = False
            error_logger.info(f'[api_curtir_comentario] Usuário {request.user.id} descurtiu comentário {comentario_id_int}')
        else:
            # Curtir - criar ou reativar curtida
            curtida_existente_inativa = CurtidaComentario.objects.filter(
                id_comentario=comentario,
                id_usuario=request.user,
                ativo=False
            ).first()
            
            if curtida_existente_inativa:
                # Reativar curtida existente
                curtida_existente_inativa.ativo = True
                curtida_existente_inativa.save()
            else:
                # Criar nova curtida
                CurtidaComentario.objects.create(
                    id_comentario=comentario,
                    id_usuario=request.user,
                    ativo=True
                )
            curtido = True
            error_logger.info(f'[api_curtir_comentario] Usuário {request.user.id} curtiu comentário {comentario_id_int}')
        
        # Retornar novo total de curtidas
        total_curtidas = comentario.curtidas.filter(ativo=True).count()
        
        return JsonResponse({
            'success': True,
            'curtido': curtido,
            'total_curtidas': total_curtidas,
            'message': 'Curtida atualizada com sucesso!'
        }, status=200)
        
    except Exception as e:
        error_logger.error(f'Erro ao curtir comentário: {str(e)}', exc_info=True)
        return JsonResponse({
            'success': False,
            'message': f'Erro ao curtir comentário: {str(e)}'
        }, status=500)

@csrf_exempt
def api_reportar_abuso(request):
    """API para reportar um comentário por abuso"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)
    
    try:
        comentario_id = request.POST.get('comentario_id')
        motivo = request.POST.get('motivo', '').strip()
        tipo = request.POST.get('tipo', 'outro')
        
        if not comentario_id:
            return JsonResponse({'success': False, 'message': 'ID do comentário não fornecido'}, status=400)
        
        try:
            comentario_id_int = int(comentario_id)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'message': 'ID do comentário inválido'}, status=400)
        
        try:
            comentario = ComentarioQuestao.objects.get(id=comentario_id_int)
        except ComentarioQuestao.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Comentário não encontrado'}, status=404)
        
        # Verificar se o usuário já reportou este comentário
        denuncia_existente = DenunciaComentario.objects.filter(
            id_comentario=comentario,
            email_usuario=request.user.email if request.user.is_authenticated else None,
            ip_usuario=get_client_ip(request)
        ).exists()
        
        if denuncia_existente:
            return JsonResponse({
                'success': False,
                'message': 'Você já reportou este comentário anteriormente.'
            }, status=400)
        
        # Criar denúncia
        denuncia = DenunciaComentario.objects.create(
            id_comentario=comentario,
            email_usuario=request.user.email if request.user.is_authenticated else None,
            ip_usuario=get_client_ip(request),
            motivo=motivo,
            tipo=tipo
        )
        
        # Marcar comentário como reportado
        comentario.reportado = True
        comentario.save()
        
        error_logger.info(f'[api_reportar_abuso] Comentário {comentario_id_int} reportado por usuário {request.user.id if request.user.is_authenticated else "anônimo"}')
        
        return JsonResponse({
            'success': True,
            'message': 'Comentário reportado com sucesso! Nossa equipe irá analisar.'
        }, status=200)
        
    except Exception as e:
        error_logger.error(f'Erro ao reportar abuso: {str(e)}', exc_info=True)
        return JsonResponse({
            'success': False,
            'message': f'Erro ao reportar comentário: {str(e)}'
        }, status=500)

def get_client_ip(request):
    """Obtém o IP do cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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