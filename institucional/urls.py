from django.urls import path
from . import views

app_name = 'institucional'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('sobre/', views.sobre_view, name='sobre'),
    path('contato/', views.contato_view, name='contato'),
    path('politica-privacidade/', views.politica_privacidade_view, name='politica_privacidade'),
    path('origem-to/', views.origem_to_view, name='origem_to'),
    path('cleice-santana/', views.cleice_santana_view, name='cleice_santana'),
    path('buscar-temas/', views.buscar_temas_view, name='buscar_temas'),  # API AJAX
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
]

