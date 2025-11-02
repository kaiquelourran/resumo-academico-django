# Arquivo: questoes/resources.py

from import_export import resources
from import_export.fields import Field
from .models import Questao, Alternativa


# =========================================================================
# 1. RESOURCE PARA O MODELO QUESTÃO
# Isso mapeia as colunas da sua planilha para o seu modelo Questao.
# =========================================================================
class QuestaoResource(resources.ModelResource):
    """Resource para importação de Questões"""
    
    class Meta:
        model = Questao
        fields = (
            'id',          # (opcional): Se preenchido, atualiza a questão existente; se vazio, cria nova com ID automático
            'texto',       # (obrigatório): Texto completo da questão
            'explicacao',  # (opcional): Explicação/justificativa
            'id_assunto',  # (obrigatório): ID do assunto (Foreign Key)
        )
        # REMOVIDO: import_id_fields = ('id',) 
        # Isso permite que o Django gere IDs automaticamente quando o campo 'id' não for fornecido no CSV
        skip_unchanged = True  # Pula linhas que não tiveram mudanças
        report_skipped = True  # Relata as linhas que foram puladas
        exclude = ('criado_em', 'atualizado_em')  # Exclui campos automáticos
    
    def before_import_row(self, row, **kwargs):
        """Método executado antes de importar cada linha - valida dados"""
        from .models import Assunto
        
        # Valida se o texto da questão foi fornecido (campo obrigatório)
        if 'texto' in row and not row.get('texto', '').strip():
            raise ValueError("O campo 'texto' é obrigatório e não pode estar vazio.")
        
        # Valida se o assunto existe
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
        else:
            raise ValueError("O campo 'id_assunto' é obrigatório e não pode estar vazio.")
        
        # Remove o campo 'id' se estiver vazio para permitir geração automática de ID
        if 'id' in row and (not row.get('id') or str(row.get('id', '')).strip() == ''):
            row['id'] = None  # None permite que o Django gere o ID automaticamente


# =========================================================================
# 2. RESOURCE PARA O MODELO ALTERNATIVA
# Importação separada de alternativas, referenciando o ID da Questão
# =========================================================================
class AlternativaResource(resources.ModelResource):
    """Resource para importação de Alternativas"""
    
    class Meta:
        model = Alternativa
        fields = (
            'id',             # (opcional): Se preenchido, atualiza a alternativa existente; se vazio, cria nova com ID automático
            'id_questao',     # (obrigatório): ID da questão (Foreign Key) - Vínculo com a Questão
            'texto',          # (obrigatório): Texto da alternativa
            'eh_correta',     # (obrigatório): Se é a alternativa correta (True/False, 1/0)
            'ordem',          # (opcional): Ordem de exibição
        )
        # REMOVIDO: import_id_fields = ('id',)
        # Isso permite que o Django gere IDs automaticamente quando o campo 'id' não for fornecido no CSV
        skip_unchanged = True
        report_skipped = True
        exclude = ('criado_em', 'atualizado_em')  # Exclui campos automáticos, se existirem
    
    def before_import_row(self, row, **kwargs):
        """Método executado antes de importar cada linha - valida dados"""
        from .models import Questao
        
        # Valida se o texto da alternativa foi fornecido (campo obrigatório)
        if 'texto' in row and not row.get('texto', '').strip():
            raise ValueError("O campo 'texto' é obrigatório e não pode estar vazio.")
        
        # Valida se a questão existe (campo obrigatório)
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
        else:
            raise ValueError("O campo 'id_questao' é obrigatório e não pode estar vazio.")
        
        # Remove o campo 'id' se estiver vazio para permitir geração automática de ID
        if 'id' in row and (not row.get('id') or str(row.get('id', '')).strip() == ''):
            row['id'] = None  # None permite que o Django gere o ID automaticamente
    
    def get_import_fields(self):
        """Retorna os campos que serão importados"""
        return self.get_fields()

