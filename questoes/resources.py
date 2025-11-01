# Arquivo: questoes/resources.py

from import_export import resources
from import_export.fields import Field
from .models import Questao, Alternativa


# =========================================================================
# 1. RESOURCE PARA O MODELO QUESTÃO
# Isso mapeia as colunas da sua planilha para o seu modelo Questao.
# =========================================================================
class QuestaoResource(resources.ModelResource):
    # Campos customizados para mapeamento de ForeignKey
    id_assunto__nome = Field(
        attribute='id_assunto__nome',
        column_name='assunto_nome',
        readonly=True
    )
    id_assunto = Field(
        attribute='id_assunto',
        column_name='assunto_id'
    )
    
    class Meta:
        model = Questao
        # Campos que o usuário provavelmente terá em sua planilha para a Questão:
        # IMPORTANTE: Os nomes das colunas no CSV devem ser exatamente estes:
        # - id (opcional): Se preenchido, atualiza a questão existente
        # - texto: Texto completo da questão (OBRIGATÓRIO)
        # - id_assunto: ID do assunto (OBRIGATÓRIO - deve existir no banco)
        # - explicacao: Explicação/justificativa (opcional)
        fields = (
            'id',
            'texto',          # Texto da questão (coluna na planilha: "texto")
            'id_assunto',     # ID do assunto (ForeignKey - coluna: "id_assunto")
            'explicacao',     # Explicação (opcional - coluna: "explicacao")
            # Campos de data são automáticos, não precisam estar na planilha
        )
        # Permite que a importação crie e atualize itens, não apenas crie.
        import_id_fields = ('id',)
        skip_unchanged = True  # Pula linhas que não tiveram mudanças
        report_skipped = True  # Relata as linhas que foram puladas
        exclude = ('criado_em', 'atualizado_em')  # Exclui campos automáticos
    
    def before_import_row(self, row, **kwargs):
        """Método executado antes de importar cada linha - valida dados"""
        from .models import Assunto
        
        # Valida se o texto da questão foi fornecido (campo obrigatório)
        if 'texto' in row and not row.get('texto', '').strip():
            raise ValueError("O campo 'texto' é obrigatório e não pode estar vazio.")
        
        # Valida se o assunto existe se for fornecido por ID
        if 'id_assunto' in row and row.get('id_assunto'):
            try:
                assunto_id = int(row['id_assunto'])
                if not Assunto.objects.filter(id=assunto_id).exists():
                    raise ValueError(f"A Foreign Key 'id_assunto={assunto_id}' não existe no banco de dados.")
            except ValueError as e:
                # Re-raise se for erro de validação do assunto
                if "não existe" in str(e):
                    raise e
                # Se não conseguir converter para int, ignora
                pass
            except (TypeError, AttributeError):
                # Se não conseguir converter para int, ignora
                pass
    
    def get_import_fields(self):
        """Retorna os campos que serão importados"""
        return self.get_fields()


# =========================================================================
# 2. RESOURCE PARA O MODELO ALTERNATIVA
# Importação separada de alternativas, referenciando o ID da Questão
# =========================================================================
class AlternativaResource(resources.ModelResource):
    # Campos customizados para mapeamento de ForeignKey
    id_questao__texto = Field(
        attribute='id_questao__texto',
        column_name='questao_texto',
        readonly=True
    )
    id_questao = Field(
        attribute='id_questao',
        column_name='questao_id'
    )
    
    class Meta:
        model = Alternativa
        fields = (
            'id',
            'id_questao',     # ID da questão (ForeignKey)
            'texto',          # Texto da alternativa
            'eh_correta',     # Se é a alternativa correta (True/False)
            'ordem',          # Ordem de exibição
        )
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True
    
    def before_import_row(self, row, **kwargs):
        """Método executado antes de importar cada linha - valida dados"""
        # Valida se o texto da alternativa foi fornecido (campo obrigatório)
        if 'texto' in row and not row.get('texto', '').strip():
            raise ValueError("O campo 'texto' é obrigatório e não pode estar vazio.")
        
        # Valida se a questão existe se for fornecido por ID
        if 'id_questao' in row and row.get('id_questao'):
            try:
                questao_id = int(row['id_questao'])
                if not Questao.objects.filter(id=questao_id).exists():
                    raise ValueError(f"A Foreign Key 'id_questao={questao_id}' não existe no banco de dados.")
            except ValueError as e:
                # Re-raise se for erro de validação da questão
                if "não existe" in str(e):
                    raise e
                # Se não conseguir converter para int, ignora
                pass
            except (TypeError, AttributeError):
                # Se não conseguir converter para int, ignora
                pass
    
    def get_import_fields(self):
        """Retorna os campos que serão importados"""
        return self.get_fields()

