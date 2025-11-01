# Generated manually to remove unique_together constraint

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questoes', '0005_criar_sistema_comentarios'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='respostausuario',
            unique_together=set(),  # Remove unique_together constraint
        ),
    ]

