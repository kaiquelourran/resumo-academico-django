# 🔐 Segurança e Privacidade - Explicação Detalhada

## 📋 ÍNDICE

1. [LGPD (Lei Geral de Proteção de Dados)](#lgpd)
2. [Autenticação de Dois Fatores (2FA)](#2fa)
3. [Configurações de Privacidade](#privacidade)
4. [Exportação de Dados](#exportacao)
5. [Outras Funcionalidades de Segurança](#outras-seguranca)

---

## 🛡️ 1. LGPD (Lei Geral de Proteção de Dados)

### O que é LGPD?

A **LGPD (Lei 13.709/2018)** é a lei brasileira que regulamenta o tratamento de dados pessoais. Ela garante que os usuários tenham controle sobre seus dados pessoais.

### Por que é importante no Resumo Acadêmico?

O sistema coleta diversos dados pessoais:
- **Dados de Cadastro**: Nome, email, senha
- **Dados de Estudo**: Respostas, estatísticas, desempenho
- **Dados de Perfil**: Foto do Google (se usar login social)
- **Dados de Interação**: Comentários, curtidas, relatórios de bug

### Funcionalidades LGPD que devem ser implementadas:

#### 1.1. **Política de Privacidade Transparente**
```
✅ Status Atual: Já existe uma página de Política de Privacidade
⚠️ Melhorias Necessárias:
   - Termos mais claros e específicos
   - Explicação de cada tipo de dado coletado
   - Como os dados são usados
   - Com quem os dados são compartilhados (se houver)
```

#### 1.2. **Consentimento Explícito**
```
📌 O que fazer:
   - Ao cadastrar, usuário deve aceitar termos explicitamente
   - Checkbox obrigatório: "Li e aceito a Política de Privacidade"
   - Permitir que usuário revise termos a qualquer momento
```

#### 1.3. **Direito de Acesso aos Dados (LGPD Art. 9º)**
```
📌 O que implementar:
   - Página "Meus Dados" mostrando todos os dados coletados
   - Visualização clara e organizada por categoria:
     * Dados Pessoais (nome, email, data de cadastro)
     * Dados de Estudo (total de respostas, estatísticas)
     * Dados de Interação (comentários feitos, relatórios enviados)
     * Dados de Sessão (último login, IP, dispositivo)
```

#### 1.4. **Direito de Correção (LGPD Art. 9º)**
```
📌 O que implementar:
   - Permitir usuário editar seus próprios dados
   - Formulário para atualizar: nome, email, senha
   - Validação para garantir integridade dos dados
```

#### 1.5. **Direito de Exclusão (LGPD Art. 9º) - "Direito ao Esquecimento"**
```
📌 O que implementar:
   - Botão "Excluir Minha Conta" na página de configurações
   - Processo em duas etapas (confirmação + confirmação final)
   - Opções de exclusão:
     * Exclusão Completa: Remove tudo (irreversível)
     * Exclusão Parcial: Mantém dados anônimos para estatísticas
   - Período de carência: 30 dias para cancelar exclusão
```

#### 1.6. **Exportação de Dados (LGPD Art. 9º)**
```
📌 O que implementar:
   - Botão "Exportar Meus Dados" na página de privacidade
   - Gerar arquivo JSON/CSV com todos os dados do usuário
   - Incluir:
     * Dados pessoais
     * Histórico completo de respostas
     * Estatísticas detalhadas
     * Comentários feitos
     * Relatórios enviados
   - Download automático ou envio por email
```

#### 1.7. **Anonimização de Dados**
```
📌 O que implementar:
   - Opção para tornar perfil anônimo
   - Dados pessoais mantidos, mas não visíveis publicamente
   - Estatísticas agregadas sem identificar usuário
```

#### 1.8. **Registro de Consentimento**
```
📌 O que implementar:
   - Armazenar quando usuário aceitou termos
   - Versão dos termos aceita
   - Histórico de mudanças de consentimento
   - Permitir revogar consentimento a qualquer momento
```

#### 1.9. **Notificação de Vazamento de Dados**
```
📌 O que implementar:
   - Sistema para detectar possíveis vazamentos
   - Notificar usuários imediatamente se houver suspeita
   - Orientar usuários sobre medidas de segurança
   - Documentar incidentes (se houver)
```

#### 1.10. **Proteção de Dados de Menores**
```
📌 O que implementar:
   - Verificação de idade (se aplicável)
   - Consentimento de responsável legal para menores
   - Proteção adicional de dados de menores
```

### Exemplo de Implementação - Página "Meus Dados"

```html
<!-- Página: /questoes/privacidade/meus-dados/ -->

<div class="privacy-container">
    <h1>🔒 Meus Dados Pessoais</h1>
    
    <!-- Seção 1: Dados Pessoais -->
    <section class="data-section">
        <h2>📝 Dados Pessoais</h2>
        <div class="data-item">
            <strong>Nome:</strong> {{ user.first_name }}
            <a href="{% url 'questoes:editar_dados' %}">Editar</a>
        </div>
        <div class="data-item">
            <strong>Email:</strong> {{ user.email }}
        </div>
        <div class="data-item">
            <strong>Data de Cadastro:</strong> {{ user.date_joined|date:"d/m/Y" }}
        </div>
        <div class="data-item">
            <strong>Último Login:</strong> {{ user.last_login|date:"d/m/Y H:i" }}
        </div>
    </section>
    
    <!-- Seção 2: Dados de Estudo -->
    <section class="data-section">
        <h2>📊 Dados de Estudo</h2>
        <div class="data-item">
            <strong>Total de Respostas:</strong> {{ total_respostas }}
        </div>
        <div class="data-item">
            <strong>Estatísticas Completas:</strong>
            <a href="{% url 'questoes:desempenho' %}">Ver Estatísticas</a>
        </div>
    </section>
    
    <!-- Seção 3: Ações -->
    <section class="actions-section">
        <h2>⚙️ Ações</h2>
        <button onclick="exportarDados()">📥 Exportar Meus Dados</button>
        <button onclick="excluirConta()" class="danger">🗑️ Excluir Minha Conta</button>
    </section>
</div>
```

---

## 🔐 2. Autenticação de Dois Fatores (2FA)

### O que é 2FA?

**2FA (Two-Factor Authentication)** adiciona uma camada extra de segurança ao login. Além da senha, o usuário precisa fornecer um segundo fator de autenticação.

### Por que é importante?

- **Proteção contra Hackers**: Mesmo que senha seja roubada, conta está protegida
- **Segurança para Contas Importantes**: Especialmente para admins e usuários com muitos dados
- **Conformidade**: Aumenta segurança e confiança dos usuários

### Tipos de 2FA que podem ser implementados:

#### 2.1. **2FA via SMS (Simples)**
```
📌 Como funciona:
   1. Usuário faz login com email/senha
   2. Sistema envia código de 6 dígitos por SMS
   3. Usuário digita código para completar login
   4. Código expira em 5 minutos

⚠️ Limitações:
   - Requer serviço de SMS (Twilio, etc.)
   - Custo por SMS enviado
   - Menos seguro que outros métodos (SIM swapping)
```

#### 2.2. **2FA via Email (Mais Simples)**
```
📌 Como funciona:
   1. Usuário faz login com email/senha
   2. Sistema envia código por email
   3. Usuário digita código para completar login
   4. Código expira em 10 minutos

✅ Vantagens:
   - Não requer serviço externo pago
   - Fácil de implementar
   - Sem custo adicional

⚠️ Limitações:
   - Menos seguro (se email for comprometido)
   - Usuário precisa acessar email
```

#### 2.3. **2FA via App Autenticador (Recomendado)**
```
📌 Como funciona:
   1. Usuário configura app autenticador (Google Authenticator, Authy, etc.)
   2. Sistema gera QR Code com chave secreta
   3. Usuário escaneia QR Code no app
   4. App gera código de 6 dígitos que muda a cada 30 segundos
   5. No login, usuário digita código do app

✅ Vantagens:
   - Mais seguro (código fica no celular)
   - Funciona offline
   - Padrão da indústria
   - Sem custo

📱 Apps Compatíveis:
   - Google Authenticator
   - Microsoft Authenticator
   - Authy
   - LastPass Authenticator
```

#### 2.4. **2FA via Backup Codes (Códigos de Emergência)**
```
📌 Como funciona:
   1. Ao ativar 2FA, sistema gera 10 códigos de backup
   2. Usuário salva códigos em local seguro
   3. Se perder acesso ao 2FA, usa código de backup
   4. Cada código só pode ser usado uma vez

✅ Vantagens:
   - Segurança adicional
   - Recuperação de acesso
```

### Fluxo de Implementação 2FA:

#### Passo 1: Ativar 2FA
```
1. Usuário vai em "Configurações > Segurança"
2. Clica em "Ativar Autenticação de Dois Fatores"
3. Escolhe método (Email ou App Autenticador)
4. Se App: Escaneia QR Code
5. Sistema gera códigos de backup
6. Usuário confirma código de teste
7. 2FA ativado
```

#### Passo 2: Login com 2FA
```
1. Usuário digita email/senha
2. Sistema verifica se 2FA está ativo
3. Se ativo: solicita código de 2FA
4. Usuário digita código (SMS/Email/App)
5. Sistema valida código
6. Login completo
```

#### Passo 3: Desativar 2FA
```
1. Usuário vai em "Configurações > Segurança"
2. Clica em "Desativar 2FA"
3. Confirma com senha atual
4. 2FA desativado
```

### Exemplo de Código Django - 2FA

```python
# models.py
class PerfilUsuario(models.Model):
    id_usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    dois_fatores_ativado = models.BooleanField(default=False)
    dois_fatores_metodo = models.CharField(
        max_length=20,
        choices=[('email', 'Email'), ('app', 'App Autenticador')],
        blank=True,
        null=True
    )
    dois_fatores_secret = models.CharField(max_length=32, blank=True, null=True)  # Para app autenticador
    dois_fatores_backup_codes = models.JSONField(default=list, blank=True)  # Códigos de backup

# views.py
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
import pyotp
import qrcode
from io import BytesIO
import base64

def ativar_2fa_view(request):
    """Ativar autenticação de dois fatores"""
    if request.method == 'POST':
        metodo = request.POST.get('metodo')  # 'email' ou 'app'
        
        if metodo == 'app':
            # Gerar secret para TOTP
            secret = pyotp.random_base32()
            
            # Salvar no perfil
            perfil = request.user.perfil
            perfil.dois_fatores_ativado = True
            perfil.dois_fatores_metodo = 'app'
            perfil.dois_fatores_secret = secret
            perfil.save()
            
            # Gerar QR Code
            totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
                name=request.user.email,
                issuer_name='Resumo Acadêmico'
            )
            
            # Criar QR Code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(totp_uri)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            # Gerar códigos de backup
            backup_codes = [secrets.token_hex(4).upper() for _ in range(10)]
            perfil.dois_fatores_backup_codes = backup_codes
            perfil.save()
            
            return render(request, 'questoes/2fa_ativado.html', {
                'qr_code': qr_code_base64,
                'backup_codes': backup_codes,
                'secret': secret
            })
        
        elif metodo == 'email':
            perfil = request.user.perfil
            perfil.dois_fatores_ativado = True
            perfil.dois_fatores_metodo = 'email'
            perfil.save()
            
            # Enviar código de teste
            codigo = gerar_codigo_2fa()
            enviar_email_2fa(request.user.email, codigo)
            
            return render(request, 'questoes/2fa_email_ativado.html', {
                'codigo_enviado': True
            })
    
    return render(request, 'questoes/ativar_2fa.html')

def login_com_2fa(request):
    """Login com verificação de 2FA"""
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        codigo_2fa = request.POST.get('codigo_2fa')
        
        user = authenticate(request, username=email, password=senha)
        
        if user:
            # Verificar se 2FA está ativo
            if user.perfil.dois_fatores_ativado:
                if not codigo_2fa:
                    # Primeira etapa: solicitar código
                    return render(request, 'questoes/login_2fa.html', {
                        'email': email,
                        'etapa': 'solicitar_codigo'
                    })
                
                # Segunda etapa: validar código
                if validar_codigo_2fa(user, codigo_2fa):
                    login(request, user)
                    return redirect('questoes:index')
                else:
                    messages.error(request, 'Código 2FA inválido')
                    return render(request, 'questoes/login_2fa.html', {
                        'email': email,
                        'etapa': 'solicitar_codigo'
                    })
            else:
                # 2FA não ativo, login normal
                login(request, user)
                return redirect('questoes:index')
        else:
            messages.error(request, 'Email ou senha incorretos')
    
    return render(request, 'questoes/login.html')

def validar_codigo_2fa(user, codigo):
    """Validar código 2FA"""
    perfil = user.perfil
    
    if perfil.dois_fatores_metodo == 'app':
        # Validar código TOTP
        totp = pyotp.TOTP(perfil.dois_fatores_secret)
        return totp.verify(codigo, valid_window=1)  # Permite 30 segundos de tolerância
    
    elif perfil.dois_fatores_metodo == 'email':
        # Validar código enviado por email (armazenado em sessão)
        codigo_sessao = request.session.get('codigo_2fa')
        return codigo == codigo_sessao
    
    # Verificar código de backup
    if codigo in perfil.dois_fatores_backup_codes:
        perfil.dois_fatores_backup_codes.remove(codigo)
        perfil.save()
        return True
    
    return False
```

---

## 🔒 3. Configurações de Privacidade

### 3.1. **Perfil Público vs Privado**

```
📌 Funcionalidade:
   - Opção: "Tornar meu perfil público"
   - Se público: outros usuários podem ver:
     * Nome de usuário
     * Estatísticas gerais (total de respostas, taxa de acerto)
     * Ranking (se permitido)
   - Se privado: apenas o próprio usuário vê seus dados

📌 Implementação:
   - Campo no PerfilUsuario: perfil_publico = BooleanField(default=False)
   - Checkbox na página de configurações
   - Filtrar dados visíveis baseado na configuração
```

### 3.2. **Visibilidade de Estatísticas**

```
📌 Funcionalidades:
   - Controlar o que é visível para outros:
     * Nome de usuário
     * Total de respostas
     * Taxa de acerto geral
     * Taxa de acerto por assunto
     * Ranking
     * Comentários
   
   - Opções:
     * "Tudo visível"
     * "Apenas estatísticas gerais"
     * "Apenas nome"
     * "Nada (perfil privado)"
```

### 3.3. **Dados Anônimos para Estatísticas**

```
📌 Funcionalidade:
   - Opção: "Contribuir com dados anônimos para estatísticas"
   - Se ativo: dados são usados para calcular médias comunitárias
   - Dados são anonimizados (sem identificar usuário)
   - Usuário pode desativar a qualquer momento
```

### 3.4. **Bloquear Usuários**

```
📌 Funcionalidade:
   - Permitir bloquear usuários específicos
   - Usuários bloqueados não podem:
     * Ver seu perfil
     * Comentar em suas questões
     * Enviar mensagens
   - Lista de usuários bloqueados na página de privacidade
```

---

## 📥 4. Exportação de Dados

### 4.1. **O que deve ser exportado?**

```
✅ Dados Pessoais:
   - Nome completo
   - Email
   - Data de cadastro
   - Último login
   - Foto de perfil (URL)

✅ Dados de Estudo:
   - Histórico completo de respostas
   - Estatísticas detalhadas
   - Taxa de acerto por assunto
   - Questões favoritas/marcadas
   - Anotações pessoais

✅ Dados de Interação:
   - Comentários feitos
   - Curtidas dadas
   - Relatórios enviados
   - Mensagens (se houver)

✅ Dados de Configurações:
   - Preferências de privacidade
   - Configurações de notificação
   - Tema escolhido
```

### 4.2. **Formatos de Exportação**

```
📌 Formatos disponíveis:
   1. JSON (estruturado, fácil de processar)
   2. CSV (para planilhas)
   3. PDF (leitura humana)
   4. XML (padrão)
```

### 4.3. **Exemplo de Estrutura JSON**

```json
{
  "usuario": {
    "nome": "João Silva",
    "email": "joao@example.com",
    "data_cadastro": "2024-01-15T10:30:00Z",
    "ultimo_login": "2025-01-20T14:20:00Z"
  },
  "estatisticas": {
    "total_respostas": 1250,
    "respostas_corretas": 850,
    "taxa_acerto_geral": 68.0,
    "por_assunto": [
      {
        "assunto": "TDAH",
        "total": 200,
        "corretas": 150,
        "taxa": 75.0
      }
    ]
  },
  "historico_respostas": [
    {
      "questao_id": 123,
      "assunto": "TDAH",
      "resposta_correta": true,
      "data": "2025-01-20T10:15:00Z"
    }
  ],
  "comentarios": [
    {
      "questao_id": 123,
      "comentario": "Ótima questão!",
      "data": "2025-01-19T08:30:00Z"
    }
  ]
}
```

---

## 🛡️ 5. Outras Funcionalidades de Segurança

### 5.1. **Histórico de Acesso**

```
📌 Funcionalidade:
   - Registrar cada login feito
   - Armazenar: IP, dispositivo, navegador, data/hora
   - Permitir usuário ver histórico
   - Alertar sobre logins suspeitos (IP diferente, localização)

📌 Exemplo de Dados Armazenados:
   - Data/Hora do login
   - Endereço IP
   - Localização aproximada (cidade, país)
   - Dispositivo (Desktop, Mobile)
   - Navegador (Chrome, Firefox, etc.)
   - Sistema Operacional
```

### 5.2. **Sessões Ativas**

```
📌 Funcionalidade:
   - Mostrar todas as sessões ativas
   - Permitir encerrar sessões remotamente
   - Útil se esqueceu de fazer logout em outro dispositivo
   
📌 Implementação:
   - Listar sessões ativas
   - Botão "Encerrar Sessão" para cada uma
   - Opção "Encerrar Todas as Outras Sessões"
```

### 5.3. **Senha Forte**

```
📌 Funcionalidade:
   - Forçar senha forte no cadastro
   - Requisitos:
     * Mínimo 8 caracteres
     * Pelo menos 1 letra maiúscula
     * Pelo menos 1 letra minúscula
     * Pelo menos 1 número
     * Pelo menos 1 caractere especial
   
   - Validação em tempo real
   - Indicador de força da senha
```

### 5.4. **Troca Periódica de Senha**

```
📌 Funcionalidade:
   - Opção para forçar troca de senha a cada X dias
   - Notificação antes de expirar
   - Histórico de senhas (para evitar reutilização)
```

### 5.5. **Login Biométrico (Mobile)**

```
📌 Funcionalidade:
   - Para apps mobile futuros
   - Login com impressão digital/Face ID
   - Mais conveniente e seguro
```

---

## 📊 RESUMO DE IMPLEMENTAÇÃO

### Prioridade Alta (LGPD Obrigatório)
1. ✅ Política de Privacidade (já existe, melhorar)
2. ⚠️ Exportação de Dados
3. ⚠️ Exclusão de Conta
4. ⚠️ Acesso aos Dados

### Prioridade Média (Segurança)
1. ⚠️ 2FA (Autenticação de Dois Fatores)
2. ⚠️ Histórico de Acesso
3. ⚠️ Sessões Ativas
4. ⚠️ Configurações de Privacidade

### Prioridade Baixa (Melhorias)
1. ⚠️ Senha Forte
2. ⚠️ Login Biométrico
3. ⚠️ Bloqueio de Usuários

---

## 🛠️ TECNOLOGIAS RECOMENDADAS

### Para 2FA:
- **django-otp**: Biblioteca Django para 2FA
- **pyotp**: Para gerar códigos TOTP
- **qrcode**: Para gerar QR Codes
- **django-allauth**: Já tem suporte básico para 2FA

### Para LGPD:
- **django-data-export**: Para exportar dados
- **django-anonymizer**: Para anonimizar dados
- **django-auditlog**: Para registrar acessos

### Para Segurança:
- **django-axes**: Para bloquear tentativas de login
- **django-session-security**: Para gerenciar sessões
- **django-password-validators**: Para validar senhas

---

## 📝 CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: LGPD Básico
- [ ] Melhorar Política de Privacidade
- [ ] Criar página "Meus Dados"
- [ ] Implementar exportação de dados (JSON)
- [ ] Implementar exclusão de conta
- [ ] Adicionar consentimento explícito no cadastro

### Fase 2: Segurança Básica
- [ ] Implementar 2FA via Email
- [ ] Implementar 2FA via App Autenticador
- [ ] Criar página de configurações de segurança
- [ ] Implementar histórico de acesso

### Fase 3: Privacidade Avançada
- [ ] Implementar configurações de privacidade
- [ ] Adicionar opção de perfil público/privado
- [ ] Implementar bloqueio de usuários
- [ ] Adicionar anonimização de dados

### Fase 4: Melhorias
- [ ] Forçar senha forte
- [ ] Implementar sessões ativas
- [ ] Adicionar notificações de segurança
- [ ] Dashboard de segurança

---

**Última atualização**: Janeiro 2025
**Versão do Documento**: 1.0

