from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Assunto, Questao, Alternativa, RespostaUsuario, RelatorioBug,
    ComentarioQuestao, CurtidaComentario, DenunciaComentario, PerfilUsuario
)
from .resources import QuestaoResource, AlternativaResource
from django.db.models import Count


class AlternativaInline(admin.TabularInline):
    model = Alternativa
    extra = 4
    fields = ('texto', 'eh_correta', 'ordem')
    verbose_name = "Alternativa"
    verbose_name_plural = "Alternativas"

@admin.register(Assunto)
class AssuntoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'tipo_assunto', 'total_questoes_display', 'criado_em')
    list_filter = ('tipo_assunto', 'criado_em')
    search_fields = ('nome',)
    ordering = ('tipo_assunto', 'nome')
    readonly_fields = ('criado_em', 'atualizado_em')
    
    def get_queryset(self, request):
        """Garante que apenas admins vejam os IDs dos assuntos"""
        qs = super().get_queryset(request)
        return qs.annotate(questoes_count=Count('questoes'))
    
    def has_module_permission(self, request):
        """Apenas admins podem acessar o módulo de Assuntos"""
        return request.user.is_staff
    
    def has_view_permission(self, request, obj=None):
        """Apenas admins podem ver os assuntos"""
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        """Apenas admins podem editar assuntos"""
        return request.user.is_staff
    
    def has_add_permission(self, request):
        """Apenas admins podem adicionar assuntos"""
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        """Apenas admins podem deletar assuntos"""
        return request.user.is_staff
    
    fieldsets = (
        ('Informações do Assunto', {
            'fields': ('nome', 'tipo_assunto')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def total_questoes_display(self, obj):
        return obj.total_questoes()
    total_questoes_display.short_description = 'Total de Questões'

@admin.register(Questao)
class QuestaoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = QuestaoResource
    # Configurações de importação
    import_template_name = 'admin/import_export/import.html'
    from_encoding = 'utf-8'  # Codificação padrão UTF-8
    
    list_display = ('id', 'id_assunto', 'texto_resumido', 'tem_explicacao', 'alternativas_count_display', 'criado_em')
    list_filter = ('id_assunto', 'criado_em')
    search_fields = ('texto', 'explicacao')
    readonly_fields = ('criado_em', 'atualizado_em', 'alternativas_count_display')
    inlines = [AlternativaInline]
    list_per_page = 50
    
    fieldsets = (
        ('Questão', {
            'fields': ('texto', 'id_assunto')
        }),
        ('Explicação (Opcional)', {
            'fields': ('explicacao',),
            'classes': ('collapse',)
        }),
        ('Estatísticas', {
            'fields': ('alternativas_count_display',),
            'classes': ('collapse',)
        }),
        ('Informações', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def texto_resumido(self, obj):
        return obj.texto[:100] + "..." if len(obj.texto) > 100 else obj.texto
    texto_resumido.short_description = 'Texto da Questão'
    
    def tem_explicacao(self, obj):
        return bool(obj.explicacao)
    tem_explicacao.short_description = 'Explicação'
    tem_explicacao.boolean = True
    
    def alternativas_count_display(self, obj):
        return obj.alternativas_count()
    alternativas_count_display.short_description = 'Nº de Alternativas'

@admin.register(Alternativa)
class AlternativaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """Admin class para o modelo Alternativa com suporte a importação/exportação"""
    resource_class = AlternativaResource  # Certifique-se de que está usando AlternativaResource
    # Configurações de importação
    import_template_name = 'admin/import_export/import_alternativa.html'  # Template customizado para alternativas
    from_encoding = 'utf-8'  # Codificação padrão UTF-8
    
    list_display = ('id', 'id_questao', 'texto_resumido', 'eh_correta', 'ordem')
    list_filter = ('eh_correta', 'id_questao__id_assunto')
    search_fields = ('texto', 'id_questao__texto')
    ordering = ('id_questao', 'ordem')
    list_per_page = 100
    
    fieldsets = (
        ('Alternativa', {
            'fields': ('id_questao', 'texto', 'eh_correta', 'ordem')
        }),
    )
    
    def texto_resumido(self, obj):
        return obj.texto[:80] + "..." if len(obj.texto) > 80 else obj.texto
    texto_resumido.short_description = 'Texto da Alternativa'

@admin.register(RespostaUsuario)
class RespostaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_nome', 'questao_resumida', 'alternativa_resumida', 'acertou_display', 'data_resposta')
    list_filter = ('acertou', 'data_resposta', 'id_questao__id_assunto')
    search_fields = ('id_questao__texto', 'id_usuario__username', 'id_usuario__first_name', 'id_usuario__email')
    readonly_fields = ('data_resposta',)
    ordering = ('-data_resposta',)
    list_per_page = 100
    date_hierarchy = 'data_resposta'
    
    fieldsets = (
        ('Resposta', {
            'fields': ('id_usuario', 'id_questao', 'id_alternativa', 'acertou')
        }),
        ('Data', {
            'fields': ('data_resposta',)
        }),
    )
    
    def usuario_nome(self, obj):
        if obj.id_usuario:
            return obj.id_usuario.first_name or obj.id_usuario.username
        return 'Anônimo'
    usuario_nome.short_description = 'Usuário'
    
    def questao_resumida(self, obj):
        return f"Q{obj.id_questao.id}: {obj.id_questao.texto[:50]}..."
    questao_resumida.short_description = 'Questão'
    
    def alternativa_resumida(self, obj):
        return obj.id_alternativa.texto[:50] + "..."
    alternativa_resumida.short_description = 'Alternativa'
    
    def acertou_display(self, obj):
        return obj.acertou
    acertou_display.short_description = 'Resultado'
    acertou_display.boolean = True

@admin.register(RelatorioBug)
class RelatorioBugAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'tipo_problema', 'status', 'prioridade', 'nome_usuario', 'tem_resposta', 'data_criacao')
    list_filter = ('tipo_problema', 'status', 'prioridade', 'usuario_viu_resposta', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'nome_usuario', 'email_usuario')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    ordering = ('-data_criacao',)
    list_per_page = 50
    date_hierarchy = 'data_criacao'
    
    fieldsets = (
        ('Informações do Relatório', {
            'fields': ('id_usuario', 'nome_usuario', 'email_usuario', 'titulo', 'descricao', 'tipo_problema', 'pagina_erro')
        }),
        ('Status e Prioridade', {
            'fields': ('status', 'prioridade')
        }),
        ('Resposta do Administrador', {
            'fields': ('resposta_admin', 'usuario_viu_resposta')
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def tem_resposta(self, obj):
        return bool(obj.resposta_admin)
    tem_resposta.short_description = 'Respondido'
    tem_resposta.boolean = True
    
    actions = ['marcar_como_resolvido', 'marcar_como_em_andamento']
    
    def marcar_como_resolvido(self, request, queryset):
        queryset.update(status='resolvido')
        self.message_user(request, f"{queryset.count()} relatórios marcados como resolvidos.")
    marcar_como_resolvido.short_description = "Marcar como Resolvido"
    
    def marcar_como_em_andamento(self, request, queryset):
        queryset.update(status='em_andamento')
        self.message_user(request, f"{queryset.count()} relatórios marcados como Em Andamento.")
    marcar_como_em_andamento.short_description = "Marcar como Em Andamento"


@admin.register(ComentarioQuestao)
class ComentarioQuestaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'questao_resumida', 'usuario_nome', 'comentario_resumido', 'ativo', 'aprovado', 'reportado', 'total_curtidas_display', 'data_comentario')
    list_filter = ('ativo', 'aprovado', 'reportado', 'data_comentario')
    search_fields = ('comentario', 'nome_usuario', 'email_usuario')
    readonly_fields = ('data_comentario',)
    ordering = ('-data_comentario',)
    list_per_page = 50
    date_hierarchy = 'data_comentario'
    
    fieldsets = (
        ('Informações do Comentário', {
            'fields': ('id_questao', 'comentario', 'id_comentario_pai')
        }),
        ('Usuário', {
            'fields': ('nome_usuario', 'email_usuario', 'id_usuario')
        }),
        ('Status', {
            'fields': ('ativo', 'aprovado', 'reportado')
        }),
        ('Data', {
            'fields': ('data_comentario',)
        }),
    )
    
    def questao_resumida(self, obj):
        return f"Q{obj.id_questao.id}: {obj.id_questao.texto[:40]}..."
    questao_resumida.short_description = 'Questão'
    
    def usuario_nome(self, obj):
        if obj.id_usuario:
            return obj.id_usuario.first_name or obj.id_usuario.username
        return obj.nome_usuario or 'Anônimo'
    usuario_nome.short_description = 'Usuário'
    
    def comentario_resumido(self, obj):
        return obj.comentario[:60] + "..." if len(obj.comentario) > 60 else obj.comentario
    comentario_resumido.short_description = 'Comentário'
    
    def total_curtidas_display(self, obj):
        return obj.total_curtidas()
    total_curtidas_display.short_description = 'Curtidas'


@admin.register(CurtidaComentario)
class CurtidaComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'comentario_resumido', 'identificacao_usuario', 'data_curtida')
    list_filter = ('data_curtida',)
    search_fields = ('email_usuario', 'id_usuario__username')
    readonly_fields = ('data_curtida',)
    ordering = ('-data_curtida',)
    
    def comentario_resumido(self, obj):
        return f"#{obj.id_comentario.id}: {obj.id_comentario.comentario[:50]}..."
    comentario_resumido.short_description = 'Comentário'
    
    def identificacao_usuario(self, obj):
        if obj.id_usuario:
            return obj.id_usuario.first_name or obj.id_usuario.username
        elif obj.email_usuario:
            return obj.email_usuario
        elif obj.ip_usuario:
            return f"IP: {obj.ip_usuario}"
        return 'Anônimo'
    identificacao_usuario.short_description = 'Usuário'


@admin.register(DenunciaComentario)
class DenunciaComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'comentario_resumido', 'tipo', 'identificacao_denunciante', 'data_denuncia')
    list_filter = ('tipo', 'data_denuncia')
    search_fields = ('motivo', 'email_usuario')
    readonly_fields = ('data_denuncia',)
    ordering = ('-data_denuncia',)
    
    def comentario_resumido(self, obj):
        return f"#{obj.id_comentario.id}: {obj.id_comentario.comentario[:50]}..."
    comentario_resumido.short_description = 'Comentário'
    
    def identificacao_denunciante(self, obj):
        if obj.email_usuario:
            return obj.email_usuario
        elif obj.ip_usuario:
            return f"IP: {obj.ip_usuario}"
        return 'Anônimo'
    identificacao_denunciante.short_description = 'Denunciante'

# Customização do Admin Site
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    """Admin para PerfilUsuario"""
    list_display = ('id_usuario', 'foto_google', 'atualizado_em')
    list_filter = ('atualizado_em',)
    search_fields = ('id_usuario__username', 'id_usuario__email', 'id_usuario__first_name')
    readonly_fields = ('atualizado_em',)
    
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('id_usuario',)
        }),
        ('Foto do Google', {
            'fields': ('foto_google',)
        }),
        ('Informações do Sistema', {
            'fields': ('atualizado_em',),
            'classes': ('collapse',)
        }),
    )

# Customização do Admin Site
admin.site.site_header = "Resumo Acadêmico - Administração"
admin.site.site_title = "Admin Resumo Acadêmico"
admin.site.index_title = "Painel de Controle"
