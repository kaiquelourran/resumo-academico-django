# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from questoes.models import RespostaUsuario, ComentarioQuestao, RelatorioBug

email = 'kaiquenunis976@gmail.com'
users = User.objects.filter(email=email).order_by('date_joined')

print("\n" + "="*80)
print("VERIFICACAO DE USUARIOS DUPLICADOS")
print("="*80)
print(f"\nEmail: {email}")
print(f"Total de usuarios: {users.count()}\n")

for user in users:
    respostas = RespostaUsuario.objects.filter(id_usuario=user).count()
    comentarios = ComentarioQuestao.objects.filter(id_usuario=user).count()
    relatorios = RelatorioBug.objects.filter(id_usuario=user).count()
    total = respostas + comentarios + relatorios
    
    print("="*80)
    print(f"USUARIO ID: {user.id}")
    print("="*80)
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Nome: {user.first_name} {user.last_name}")
    print(f"Ativo: {user.is_active}")
    print(f"Criado em: {user.date_joined}")
    print(f"Ultimo login: {user.last_login}")
    print(f"\nDADOS ASSOCIADOS:")
    print(f"  - Respostas: {respostas}")
    print(f"  - Comentarios: {comentarios}")
    print(f"  - Relatorios: {relatorios}")
    print(f"  - TOTAL: {total} registros")
    print()

print("="*80)
print("RECOMENDACAO:")
print("="*80)
print("Mantenha o usuario com MAIS dados associados.")
print("Se ambos tiverem a mesma quantidade, mantenha o mais antigo.")
print("="*80 + "\n")

