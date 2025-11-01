from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Assunto(models.Model):
    """Modelo para os assuntos/temas das questões"""
    
    TIPO_CHOICES = [
        ('tema', 'Tema'),
        ('concurso', 'Concurso'),
        ('profissional', 'Profissional'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name="Nome do Assunto")
    tipo_assunto = models.CharField(max_length=20, choices=TIPO_CHOICES, default='tema', verbose_name="Tipo")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    # Campos específicos para concursos
    concurso_ano = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ano do Concurso")
    concurso_banca = models.CharField(max_length=100, blank=True, null=True, verbose_name="Banca")
    concurso_orgao = models.CharField(max_length=100, blank=True, null=True, verbose_name="Órgão")
    concurso_prova = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tipo de Prova")
    
    class Meta:
        verbose_name = "Assunto"
        verbose_name_plural = "Assuntos"
        ordering = ['tipo_assunto', 'nome']
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_assunto_display()})"
    
    def total_questoes(self):
        """Retorna o total de questões deste assunto"""
        return self.questoes.count()
    
    def info_concurso(self):
        """Retorna informações do concurso em formato legível"""
        if self.tipo_assunto != 'concurso' or not any([self.concurso_ano, self.concurso_banca, self.concurso_orgao]):
            return ""
        
        parts = []
        if self.concurso_orgao:
            parts.append(self.concurso_orgao)
        if self.concurso_ano:
            parts.append(self.concurso_ano)
        if self.concurso_banca:
            parts.append(self.concurso_banca)
        
        return " - ".join(parts)


class Questao(models.Model):
    """Modelo para armazenar questões do quiz"""
    
    texto = models.TextField(verbose_name="Texto da Questão")
    id_assunto = models.ForeignKey(
        Assunto, 
        on_delete=models.CASCADE, 
        related_name='questoes',
        verbose_name="Assunto"
    )
    explicacao = models.TextField(blank=True, null=True, verbose_name="Explicação")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Questão {self.id}: {self.texto[:50]}..."
    
    def get_absolute_url(self):
        """URL para a questão - necessário para django-comments-xtd"""
        # Retorna a URL da página do quiz vertical com a questão específica
        # Se houver uma view de detalhe, use: return reverse('questoes:detalhe_questao', args=[self.id])
        # Por enquanto, retornamos a URL do quiz vertical filtrado por assunto
        if self.id_assunto:
            return reverse('questoes:quiz_vertical_filtros', args=[self.id_assunto.id]) + f'?questao_inicial={self.id}'
        return reverse('questoes:index')
    
    def alternativas_count(self):
        """Retorna o total de alternativas"""
        return self.alternativas.count()


class Alternativa(models.Model):
    """Modelo para as alternativas de cada questão"""
    
    id_questao = models.ForeignKey(
        Questao, 
        on_delete=models.CASCADE, 
        related_name='alternativas',
        verbose_name="Questão"
    )
    texto = models.TextField(verbose_name="Texto da Alternativa")
    eh_correta = models.BooleanField(default=False, verbose_name="É correta?")
    ordem = models.IntegerField(default=0, verbose_name="Ordem de Exibição")
    
    class Meta:
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"
        ordering = ['ordem', 'id']
    
    def __str__(self):
        return f"{self.id_questao} - {self.texto[:50]}..."


class RespostaUsuario(models.Model):
    """Modelo para armazenar as respostas dos usuários"""
    
    id_usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Usuário"
    )
    id_questao = models.ForeignKey(
        Questao, 
        on_delete=models.CASCADE,
        verbose_name="Questão"
    )
    id_alternativa = models.ForeignKey(
        Alternativa,
        on_delete=models.CASCADE,
        verbose_name="Alternativa Escolhida"
    )
    acertou = models.BooleanField(default=False, verbose_name="Acertou?")
    data_resposta = models.DateTimeField(auto_now_add=True, verbose_name="Data da Resposta")
    
    class Meta:
        verbose_name = "Resposta do Usuário"
        verbose_name_plural = "Respostas dos Usuários"
        ordering = ['-data_resposta']
        # Removido unique_together para permitir histórico de múltiplas respostas
        # unique_together = ['id_usuario', 'id_questao']
    
    def __str__(self):
        status = "✓" if self.acertou else "✗"
        return f"{status} Questão {self.id_questao_id} - {self.data_resposta}"


class RelatorioBug(models.Model):
    """Modelo para relatórios de bugs e sugestões"""
    
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('resolvido', 'Resolvido'),
        ('fechado', 'Fechado'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    TIPO_CHOICES = [
        ('bug', 'Bug'),
        ('melhoria', 'Melhoria'),
        ('duvida', 'Dúvida'),
        ('outro', 'Outro'),
    ]
    
    id_usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuário"
    )
    nome_usuario = models.CharField(max_length=200, verbose_name="Nome do Usuário")
    email_usuario = models.EmailField(verbose_name="E-mail do Usuário")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    tipo_problema = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='bug',
        verbose_name="Tipo de Problema"
    )
    pagina_erro = models.CharField(max_length=500, blank=True, null=True, verbose_name="Página do Erro")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto',
        verbose_name="Status"
    )
    prioridade = models.CharField(
        max_length=20,
        choices=PRIORIDADE_CHOICES,
        default='media',
        verbose_name="Prioridade"
    )
    resposta_admin = models.TextField(blank=True, null=True, verbose_name="Resposta do Admin")
    usuario_viu_resposta = models.BooleanField(default=False, verbose_name="Usuário viu a resposta?")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    
    class Meta:
        verbose_name = "Relatório de Bug"
        verbose_name_plural = "Relatórios de Bugs"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"[{self.get_tipo_problema_display()}] {self.titulo} - {self.get_status_display()}"


# ==========================================
# MODELOS DE COMENTÁRIOS E INTERAÇÕES
# ==========================================

class ComentarioQuestao(models.Model):
    """Modelo para comentários de questões"""
    
    id_questao = models.ForeignKey(
        Questao,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name="Questão"
    )
    nome_usuario = models.CharField(max_length=150, verbose_name="Nome do Usuário")
    email_usuario = models.EmailField(blank=True, null=True, verbose_name="E-mail do Usuário")
    id_usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Usuário (Autenticado)"
    )
    comentario = models.TextField(verbose_name="Comentário")
    id_comentario_pai = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='respostas',
        verbose_name="Comentário Pai"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo?")
    aprovado = models.BooleanField(default=True, verbose_name="Aprovado?")
    reportado = models.BooleanField(default=False, verbose_name="Reportado?")
    data_comentario = models.DateTimeField(auto_now_add=True, verbose_name="Data do Comentário")
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-data_comentario']
    
    def __str__(self):
        return f"Comentário #{self.id} em Questão #{self.id_questao_id}"
    
    def total_curtidas(self):
        """Retorna total de curtidas"""
        return self.curtidas.count()
    
    def total_respostas(self):
        """Retorna total de respostas"""
        return self.respostas.filter(ativo=True, aprovado=True).count()


class CurtidaComentario(models.Model):
    """Modelo para curtidas em comentários"""
    
    id_comentario = models.ForeignKey(
        ComentarioQuestao,
        on_delete=models.CASCADE,
        related_name='curtidas',
        verbose_name="Comentário"
    )
    id_usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Usuário"
    )
    email_usuario = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    ip_usuario = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP")
    ativo = models.BooleanField(default=True, verbose_name="Ativo?")
    data_curtida = models.DateTimeField(auto_now_add=True, verbose_name="Data da Curtida")
    
    class Meta:
        verbose_name = "Curtida"
        verbose_name_plural = "Curtidas"
        ordering = ['-data_curtida']
    
    def __str__(self):
        return f"Curtida #{self.id} no Comentário #{self.id_comentario_id}"


class DenunciaComentario(models.Model):
    """Modelo para denúncias de comentários"""
    
    TIPO_CHOICES = [
        ('spam', 'Spam'),
        ('inapropriado', 'Conteúdo Inapropriado'),
        ('bullying', 'Bullying'),
        ('outro', 'Outro'),
    ]
    
    id_comentario = models.ForeignKey(
        ComentarioQuestao,
        on_delete=models.CASCADE,
        related_name='denuncias',
        verbose_name="Comentário"
    )
    email_usuario = models.EmailField(blank=True, null=True, verbose_name="E-mail do Denunciante")
    ip_usuario = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP do Denunciante")
    motivo = models.TextField(blank=True, null=True, verbose_name="Motivo")
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        blank=True,
        null=True,
        verbose_name="Tipo"
    )
    data_denuncia = models.DateTimeField(auto_now_add=True, verbose_name="Data da Denúncia")
    
    class Meta:
        verbose_name = "Denúncia"
        verbose_name_plural = "Denúncias"
        ordering = ['-data_denuncia']
    
    def __str__(self):
        return f"Denúncia #{self.id} no Comentário #{self.id_comentario_id}"
