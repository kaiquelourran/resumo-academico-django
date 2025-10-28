/**
 * Sistema de Quiz - Funcionalidades JavaScript
 * Versão: Vertical com Filtros (Gemini Consolidation)
 */

// Variáveis globais (se necessário, mas evite no sistema vertical)
let pontuacaoTotal = 0;

// --- FUNÇÕES DE UTILIDADE ---

// Função auxiliar para obter cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Função para exibir feedback de toast
function exibirFeedback(mensagem, sucesso) {
    // Remover toast anterior se existir
    const toastAnterior = document.querySelector('.quiz-toast');
    if (toastAnterior) {
        toastAnterior.remove();
    }
    
    // Criar novo toast
    const toast = document.createElement('div');
    toast.className = `quiz-toast ${sucesso ? 'success' : 'error'}`;
    toast.textContent = mensagem;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${sucesso ? '#4caf50' : '#f44336'};
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    // Remover após 3 segundos
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Função para mostrar explicação
function mostrarExplicacao(questaoCard, explicacao) {
    let explicacaoContainer = questaoCard.querySelector('.explicacao-container');
    
    if (!explicacaoContainer) {
        explicacaoContainer = document.createElement('div');
        explicacaoContainer.className = 'explicacao-container';
        explicacaoContainer.innerHTML = `
            <div class="explicacao-title">💡 Explicação:</div>
            <div class="explicacao-text">${explicacao}</div>
        `;
        
        // Assume que o formulário está dentro ou logo antes da explicação
        const form = questaoCard.querySelector('.questoes-form');
        if (form && form.parentNode) {
            form.parentNode.insertBefore(explicacaoContainer, form.nextSibling);
        }
    }
}

// Função para desativar alternativas após resposta
function desativarAlternativas(questaoId) {
    const questaoCard = document.querySelector(`#questao-${questaoId}`);
    if (!questaoCard) return;
    
    // Desativa apenas as alternativas do card específico
    const alternativas = questaoCard.querySelectorAll('.alternative');
    alternativas.forEach(alt => {
        alt.style.pointerEvents = 'none';
        alt.style.cursor = 'default';
        alt.style.opacity = '0.7';
    });
}

// --- FUNÇÕES DE FEEDBACK E ESTADO ---

// Função para mostrar feedback visual
function mostrarFeedback(questaoId, data) {
    const questaoCard = document.querySelector(`#questao-${questaoId}`);
    
    if (!questaoCard) {
        console.error('Questão não encontrada:', questaoId);
        return;
    }
    
    const alternativas = questaoCard.querySelectorAll('.alternative');
    
    // Limpar feedback anterior
    alternativas.forEach(alt => {
        alt.classList.remove('alternative-correct', 'alternative-incorrect-chosen');
    });
    
    // Aplicar feedback baseado na resposta
    alternativas.forEach(alt => {
        const alternativaId = parseInt(alt.dataset.alternativaId);
        
        // Se a alternativa é a correta (baseado no ID retornado pelo backend)
        if (alternativaId === data.id_alternativa_correta) {
            alt.classList.add('alternative-correct');
        } 
        
        // Se foi a alternativa escolhida E estava incorreta
        else if (!data.acertou && alternativaId === data.id_alternativa_selecionada) {
             alt.classList.add('alternative-incorrect-chosen');
        }
    });
    
    // Mostrar explicação se disponível
    if (data.explicacao && data.explicacao.trim() !== '') {
        setTimeout(() => {
            mostrarExplicacao(questaoCard, data.explicacao);
        }, 500);
    }
    
    // Exibir feedback de toast
    if (data.acertou) {
        exibirFeedback("Correto! 😄", true);
    } else {
        exibirFeedback("Incorreto! 😥", false);
    }

    // 🌟 LÓGICA DE FILTRO: ATUALIZAÇÃO E APLICAÇÃO 🌟
    // 1. Marca o card da questão com o novo status
    questaoCard.dataset.statusResposta = data.acertou ? 'correta' : 'incorreta';

    // 2. Atualiza os contadores no filtro
    atualizarContadores();

    // 3. Re-aplica o filtro atual (para esconder/mostrar se necessário)
    const filtroAtual = localStorage.getItem('filtro_ativo') || 'todas';
    aplicarFiltro(filtroAtual);
}

// --- LÓGICA DE FILTRAGEM ---

// Função que itera sobre todos os cards e aplica o filtro
function aplicarFiltro(filtro) {
    const todosCards = document.querySelectorAll('.question-card');
    
    // Salva o filtro no armazenamento local
    localStorage.setItem('filtro_ativo', filtro); 

    todosCards.forEach(card => {
        // Pega o status do atributo de dados. Se não existir, é 'nao-respondida'.
        const status = card.dataset.statusResposta || 'nao-respondida';
        let deveMostrar = false;

        switch (filtro) {
            case 'todas':
                deveMostrar = true;
                break;
            case 'corretas':
                deveMostrar = (status === 'correta');
                break;
            case 'incorretas':
                deveMostrar = (status === 'incorreta');
                break;
            case 'nao-respondidas':
                deveMostrar = (status === 'nao-respondida');
                break;
        }

        // Se deve mostrar, usamos 'block' para o layout vertical padrão
        card.style.display = deveMostrar ? 'block' : 'none'; 
    });
    
    // Atualiza o estado visual dos botões de filtro
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filtro === filtro);
    });
}

// Função auxiliar para recalcular e atualizar os contadores 
function atualizarContadores() {
    const todosCards = document.querySelectorAll('.question-card');
    let contCorretas = 0;
    let contIncorretas = 0;
    let contNaoRespondidas = 0;
    
    todosCards.forEach(card => {
        const status = card.dataset.statusResposta || 'nao-respondida';
        
        if (status === 'correta') {
            contCorretas++;
        } else if (status === 'incorreta') {
            contIncorretas++;
        } else {
            contNaoRespondidas++;
        }
    });
    
    // 🌟 ATUALIZE OS ELEMENTOS HTML AQUI (Certifique-se que estes IDs existem) 🌟
    const totalElement = document.querySelector('#contador-total');
    if (totalElement) totalElement.textContent = todosCards.length;
    
    const corretasElement = document.querySelector('#contador-corretas');
    if (corretasElement) corretasElement.textContent = contCorretas;

    const incorretasElement = document.querySelector('#contador-incorretas');
    if (incorretasElement) incorretasElement.textContent = contIncorretas;
    
    const naoRespondidasElement = document.querySelector('#contador-nao-respondidas');
    if (naoRespondidasElement) naoRespondidasElement.textContent = contNaoRespondidas;
}


// --- INICIALIZAÇÃO E EVENT LISTENERS ---

document.addEventListener('DOMContentLoaded', function() {
    const alternativas = document.querySelectorAll('.alternative');
    
    // --- 1. Event Listeners das Alternativas (Lógica AJAX) ---
    alternativas.forEach(alternativa => {
        alternativa.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const questaoId = this.dataset.questaoId;
            const alternativaId = this.dataset.alternativaId;
            const questaoCard = this.closest('.question-card');
            
            // Verificar se já foi respondida 
            if (questaoCard.dataset.statusResposta) {
                exibirFeedback("Questão já respondida!", false);
                return;
            }
            
            // Desativar alternativas para evitar cliques duplos
            desativarAlternativas(questaoId);
            
            // Enviar resposta via AJAX
            // 🚨 AJUSTE DE URL AQUI! USAMOS A URL QUE APARECEU NO SEU LOG.
            fetch('/questoes/quiz/validar/', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    // Usamos id_questao e id_alternativa para coincidir com a provável configuração do seu Django
                    id_questao: parseInt(questaoId), 
                    id_alternativa: parseInt(alternativaId) 
                })
            })
            .then(response => {
                // Tratamento de erro 400 Bad Request e outros erros de rede/servidor
                if (!response.ok) {
                    // Tenta ler a mensagem de erro do backend para o console
                    return response.json().then(data => {
                        throw new Error(`Erro ${response.status}: ${data.erro || 'Requisição falhou.'}`);
                    }).catch(() => {
                        throw new Error(`Erro de rede ou servidor: ${response.status}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.sucesso !== undefined && data.sucesso) {
                    mostrarFeedback(questaoId, data);
                } else if (data.erro) {
                    // Reativa alternativas se o backend falhou após o salvamento
                    const card = document.querySelector(`#questao-${questaoId}`);
                    card.dataset.statusResposta = ''; 
                    exibirFeedback(`Erro: ${data.erro}`, false);
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                exibirFeedback(`Erro ao salvar resposta: ${error.message}`, false);
                // Em caso de erro, reativar as alternativas
                const card = document.querySelector(`#questao-${questaoId}`);
                if (card) {
                    card.dataset.statusResposta = ''; 
                    // Se o card não tiver sido marcado, reativa
                    if (!card.dataset.statusResposta) {
                       const alternativasDoCard = card.querySelectorAll('.alternative');
                       alternativasDoCard.forEach(alt => {
                           alt.style.pointerEvents = 'auto';
                           alt.style.cursor = 'pointer';
                           alt.style.opacity = '1';
                       });
                    }
                }
            });
        });
    });
    
    // --- 2. Event Listeners dos Filtros ---
    
    // Inicializa os filtros com base no que foi salvo ou 'todas'
    const filtroInicial = localStorage.getItem('filtro_ativo') || 'todas';
    aplicarFiltro(filtroInicial);
    
    // Adiciona o listener para os botões de filtro (class="filter-btn" data-filtro="...")
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const filtro = this.dataset.filtro;
            aplicarFiltro(filtro);
        });
    });
    
    // Atualiza os contadores ao carregar a página
    atualizarContadores();

});