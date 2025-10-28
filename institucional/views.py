from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.db import models

def index_view(request):
    """Página inicial do site"""
    return render(request, 'institucional/index.html')


def sobre_view(request):
    """Página Sobre Nós"""
    return render(request, 'institucional/sobre.html')


def contato_view(request):
    """Página de Contato - Processa o formulário"""
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip().lower()
        assunto = request.POST.get('assunto', '')
        mensagem = request.POST.get('mensagem', '').strip()
        
        # Validações
        if not nome or not email or not assunto or not mensagem:
            messages.error(request, 'Por favor, preencha todos os campos.')
        else:
            # Validar email
            if '@' not in email or '.' not in email:
                messages.error(request, 'Por favor, insira um e-mail válido.')
            else:
                # Mapear códigos de assunto para nomes legíveis
                assunto_map = {
                    'duvida': 'Dúvida sobre o Sistema',
                    'sugestao': 'Sugestão de Melhoria',
                    'problema': 'Reportar Problema',
                    'parceria': 'Proposta de Parceria',
                    'outro': 'Outro'
                }
                assunto_nome = assunto_map.get(assunto, 'Outro')
                
                # Aqui você pode implementar:
                # - Envio de email via Django's email backend
                # - Salvar em banco de dados (se necessário)
                # - Log de contatos
                
                # Por enquanto, apenas confirmamos o recebimento
                messages.success(
                    request, 
                    f'Obrigado pelo seu contato, {nome}! Recebemos sua mensagem sobre "{assunto_nome}" e responderemos em breve.'
                )
    
    return render(request, 'institucional/contato.html')


def politica_privacidade_view(request):
    """Página de Política de Privacidade"""
    return render(request, 'institucional/politica_privacidade.html')


def buscar_temas_view(request):
    """API AJAX para buscar temas"""
    from questoes.models import Assunto
    
    try:
        # Buscar temas com pelo menos 1 questão
        assuntos = Assunto.objects.annotate(
            total_questoes=models.Count('questoes')
        ).filter(
            models.Q(tipo_assunto='tema') | models.Q(tipo_assunto__isnull=True),
            total_questoes__gt=0
        ).order_by('nome')[:12]
        
        temas = [
            {
                'id_assunto': a.id,
                'nome': a.nome,
                'total_questoes': a.total_questoes
            }
            for a in assuntos
        ]
        
        return JsonResponse(temas, safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)


def origem_to_view(request):
    """Página sobre a origem da Terapia Ocupacional"""
    return render(request, 'institucional/origem_to.html')


def cleice_santana_view(request):
    """Página de Currículo da Cleice Santana"""
    return render(request, 'institucional/cleice_santana.html')


def sitemap_view(request):
    """Sitemap XML para SEO"""
    return render(request, 'institucional/sitemap.xml', content_type='application/xml')
