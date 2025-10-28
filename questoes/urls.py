from django.urls import path
from . import views

app_name = 'questoes'

urlpatterns = [
    # Página inicial
    path('index/', views.index_view, name='index'),
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
   
    
    # Desempenho do usuário
    path('desempenho/', views.desempenho_view, name='desempenho'),
    
    # Gerenciar questões (admin)
    path('gerenciar/', views.gerenciar_questoes_view, name='gerenciar_questoes'),
    path('adicionar/', views.adicionar_questao_view, name='adicionar_questao'),
    path('editar/<int:questao_id>/', views.editar_questao_view, name='editar_questao'),
    path('deletar/', views.deletar_questao_view, name='deletar_questao'),
    
    # Gerenciar assuntos (admin)
    path('gerenciar-assuntos/', views.gerenciar_assuntos_view, name='gerenciar_assuntos'),
    path('adicionar-assunto/', views.adicionar_assunto_view, name='adicionar_assunto'),
    path('deletar-assunto/', views.deletar_assunto_view, name='deletar_assunto'),
    
    # Gerenciar comentários (admin)
    path('gerenciar-comentarios/', views.gerenciar_comentarios_view, name='gerenciar_comentarios'),
    path('toggle-comentario/<int:comentario_id>/', views.alternar_status_comentario_view, name='alternar_status_comentario'),
    path('deletar-comentario/<int:comentario_id>/', views.deletar_comentario_view, name='deletar_comentario'),
    
    # Página inicial - escolher assunto
    path('', views.escolher_assunto_view, name='escolher_assunto'),
    
    # Listar questões de um assunto com filtros
    path('assunto/<int:assunto_id>/', views.listar_questoes_view, name='listar_questoes'),
    
    # Quiz com questões do assunto escolhido
    path('quiz/<int:assunto_id>/', views.quiz_view, name='quiz'),
    
    # Rota para validar as respostas (endpoint de API)
    path('quiz/validar/', views.validar_resposta_view, name='validar_resposta'),
    
    # APIs REST
    path('api/comentarios/', views.api_comentarios, name='api_comentarios'),
    path('api/estatisticas/', views.api_estatisticas, name='api_estatisticas'),
    
    # Relatar problema
    path('relatar-problema/', views.relatar_problema_view, name='relatar_problema'),
    
    # API de notificações
    path('api/notificacoes/', views.api_notificacoes, name='api_notificacoes'),
    
    # Dashboard de administração
    path('admin/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # Gerenciar relatórios (admin)
    path('gerenciar-relatorios/', views.gerenciar_relatorios_view, name='gerenciar_relatorios'),
    path('atualizar-status-relatorio/<int:relatorio_id>/', views.atualizar_status_relatorio_view, name='atualizar_status_relatorio'),
    path('responder-relatorio/', views.responder_relatorio_view, name='responder_relatorio'),
    
    # Gerenciar usuários (admin)
    path('gerenciar-usuarios/', views.gerenciar_usuarios_view, name='gerenciar_usuarios'),
    
    # Login administrativo
    path('admin/login/', views.admin_login_view, name='admin_login'),
]
# No final do arquivo questoes/views.py

from django.shortcuts import redirect, render # Garanta que estas importações estão no topo do arquivo

# 1. Função que resolve o último erro mostrado: validar_resposta_view
def validar_resposta_view(request):
    """Placeholder para a view que processa a resposta do quiz."""
    # Sua lógica de validação deve ir aqui
    if request.method == 'POST':
        pass 
    return redirect('questoes:index') # Redireciona para o índice ou outra página

# 2. Função mencionada que precisa existir: quiz_view
def quiz_view(request, assunto_id):
    """Placeholder para a view que carrega a página do quiz."""
    # Sua lógica para carregar as questões do assunto_id deve ir aqui
    return render(request, 'questoes/quiz.html', {}) # Retorna a página do quiz