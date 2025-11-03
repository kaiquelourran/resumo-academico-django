from .models import RelatorioBug

def notificacoes_globais(request):
    """Context processor para disponibilizar notificações em todos os templates"""
    notificacoes = []
    if request.user.is_authenticated:
        notificacoes = RelatorioBug.objects.filter(
            id_usuario=request.user, 
            resposta_admin__isnull=False,
            resposta_admin__gt='',
            usuario_viu_resposta=False
        ).order_by('-data_atualizacao')[:5]
    
    return {
        'notificacoes_globais': notificacoes,
        'total_notificacoes': len(notificacoes)
    }

