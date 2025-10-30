import django_filters
from .models import Questao, Assunto

class QuestaoFilter(django_filters.FilterSet):
    """
    Define os filtros utilizados para o modelo Questao.
    Permite buscar texto no corpo da questão e filtrar por assunto ou tipo.
    """

    # Busca textual no campo 'texto'
    texto = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Buscar na Questão (conteúdo)',
    )

    # Filtra pelo tipo de assunto (campo relacionado no modelo Assunto)
    tipo_assunto = django_filters.ChoiceFilter(
        field_name='id_assunto__tipo_assunto',
        choices=Assunto.TIPO_CHOICES,
        empty_label='Todos os Tipos',
        label='Filtrar por Tipo'
    )

    # Filtra por um assunto específico
    assunto = django_filters.ModelChoiceFilter(
        field_name='id_assunto',
        queryset=Assunto.objects.all().order_by('nome'),
        empty_label='Todos os Assuntos',
        label='Filtrar por Assunto'
    )

    class Meta:
        model = Questao
        fields = ['texto', 'tipo_assunto', 'assunto']

