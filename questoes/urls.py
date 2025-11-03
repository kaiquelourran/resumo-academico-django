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
    path('relatorio-topico/<int:assunto_id>/', views.relatorio_topico_view, name='relatorio_topico'),
    path('quiz-erros-frequentes/', views.quiz_erros_frequentes_view, name='quiz_erros_frequentes'),
    
    # Gerenciar questões (admin)
    path('gerenciar/', views.gerenciar_questoes_view, name='gerenciar_questoes'),
    path('gerenciar-assuntos/', views.gerenciar_assuntos_view, name='gerenciar_assuntos'),
    path('adicionar-assunto/', views.adicionar_assunto_view, name='adicionar_assunto'),
    path('deletar-assunto/', views.deletar_assunto_view, name='deletar_assunto'),
    path('adicionar/', views.adicionar_questao_view, name='adicionar_questao'),
    path('editar/<int:questao_id>/', views.editar_questao_view, name='editar_questao'),
    path('deletar/', views.deletar_questao_view, name='deletar_questao'),
    path('deletar-todas-assunto/', views.deletar_todas_questoes_assunto_view, name='deletar_todas_questoes_assunto'),
    
    # Página inicial - escolher assunto
    path('', views.escolher_assunto_view, name='escolher_assunto'),
    
    # Rotas de Quiz
    path('assunto/<int:assunto_id>/', views.quiz_view, name='quiz'),
    # Rota Corrigida (Lista de questões com filtros via JS/Queryset)
    path('listar/<int:assunto_id>/', views.listar_questoes_view, name='listar_questoes'),
    
    # Quiz vertical com filtros dinâmicos
    path('quiz-vertical/<int:assunto_id>/', views.quiz_vertical_filtros_view, name='quiz_vertical_filtros'),
    
    # Simulado online com todas as questões em uma página
    path('simulado/<int:assunto_id>/', views.simulado_online_view, name='simulado_online'),
    # Estatísticas por questão
    path('<int:questao_id>/estatisticas/', views.estatisticas_questao, name='estatisticas'),
    
    # Rota para validar as respostas (endpoint de API)
    path('quiz/validar/', views.validar_resposta_view, name='validar_resposta'),
    
    # APIs REST
    path('comentarios/api/', views.api_comentarios, name='api_comentarios'),
    path('comentarios/criar/', views.api_criar_comentario, name='api_criar_comentario'),
    path('comentarios/curtir/', views.api_curtir_comentario, name='api_curtir_comentario'),
    path('comentarios/reportar/', views.api_reportar_abuso, name='api_reportar_abuso'),
    path('api/estatisticas/', views.api_estatisticas, name='api_estatisticas'),
    
    # Relatar problema
    path('relatar-problema/', views.relatar_problema_view, name='relatar_problema'),
    
    # API de notificações
    path('api/notificacoes/', views.api_notificacoes, name='api_notificacoes'),
    
    # Dashboard de administração
    path('admin/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # Login administrativo
    path('admin/login/', views.admin_login_view, name='admin_login'),
    
    # Gerenciar comentários (admin)
    path('admin/gerenciar-comentarios/', views.gerenciar_comentarios_view, name='gerenciar_comentarios'),
    path('admin/comentarios/<int:comentario_id>/toggle/', views.toggle_comentario_view, name='toggle_comentario'),
    path('admin/comentarios/<int:comentario_id>/deletar/', views.deletar_comentario_view, name='deletar_comentario'),
]