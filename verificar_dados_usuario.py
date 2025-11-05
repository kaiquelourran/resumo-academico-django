"""
Script para verificar dados associados a usuários duplicados.
Execute com: python manage.py shell < verificar_dados_usuario.py
Ou copie e cole cada bloco no shell do Django.
"""

from django.contrib.auth.models import User
from questoes.models import RespostaUsuario, ComentarioQuestao, RelatorioBug

print("\n" + "="*80)
print("VERIFICAÇÃO DE USUÁRIOS DUPLICADOS E SEUS DADOS ASSOCIADOS")
print("="*80 + "\n")

# Email duplicado conhecido
email = 'kaiquenunis976@gmail.com'
users = User.objects.filter(email=email).order_by('date_joined')

print(f"📧 Email: {email}")
print(f"👥 Total de usuários: {users.count()}\n")

for user in users:
    print(f"\n{'='*80}")
    print(f"👤 USUÁRIO ID: {user.id}")
    print(f"{'='*80}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Nome: {user.first_name} {user.last_name}")
    print(f"Ativo: {user.is_active}")
    print(f"Staff: {user.is_staff}")
    print(f"Criado em: {user.date_joined}")
    print(f"Último login: {user.last_login}")
    
    # Verificar dados associados
    respostas_count = RespostaUsuario.objects.filter(id_usuario=user).count()
    comentarios_count = ComentarioQuestao.objects.filter(id_usuario=user).count()
    relatorios_count = RelatorioBug.objects.filter(id_usuario=user).count()
    
    print(f"\n📊 DADOS ASSOCIADOS:")
    print(f"  - Respostas de questões: {respostas_count}")
    print(f"  - Comentários: {comentarios_count}")
    print(f"  - Relatórios de bugs: {relatorios_count}")
    
    total_dados = respostas_count + comentarios_count + relatorios_count
    print(f"  - TOTAL: {total_dados} registros")
    
    if total_dados > 0:
        print(f"\n  ⚠️  Este usuário tem dados associados!")
        print(f"     Se você deletá-lo, todos esses dados serão perdidos!")

print("\n" + "="*80)
print("RECOMENDAÇÃO:")
print("="*80)
print("Mantenha o usuário que tem MAIS dados associados.")
print("Se ambos tiverem a mesma quantidade, mantenha o mais antigo (primeiro criado).")
print("="*80 + "\n")

# Verificar todos os emails duplicados no sistema
print("\n" + "="*80)
print("TODOS OS EMAILS COM MÚLTIPLOS USUÁRIOS")
print("="*80 + "\n")

from django.db.models import Count

duplicates = User.objects.values('email').annotate(count=Count('email')).filter(count__gt=1).order_by('-count')

if duplicates.exists():
    print(f"Total de emails com duplicados: {duplicates.count()}\n")
    
    for dup in duplicates:
        email = dup['email']
        count = dup['count']
        users_dup = User.objects.filter(email=email).order_by('date_joined')
        
        print(f"\n📧 Email: {email} - {count} usuário(s)")
        for u in users_dup:
            respostas = RespostaUsuario.objects.filter(id_usuario=u).count()
            comentarios = ComentarioQuestao.objects.filter(id_usuario=u).count()
            relatorios = RelatorioBug.objects.filter(id_usuario=u).count()
            total = respostas + comentarios + relatorios
            
            print(f"  - ID: {u.id}, Username: {u.username}, Criado: {u.date_joined}")
            print(f"    Dados: {total} registros (Respostas: {respostas}, Comentários: {comentarios}, Relatórios: {relatorios})")
else:
    print("Nenhum outro email duplicado encontrado (exceto o caso acima).")

print("\n" + "="*80 + "\n")

