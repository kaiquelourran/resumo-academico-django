/**
 * Sistema de Quiz - Funcionalidades JavaScript
 */

let pontuacaoTotal = 0;
let questaoAtual = 1;

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
        const ehCorreta = alt.dataset.correta === 'true';
        
        if (data.acertou && ehCorreta) {
            alt.classList.add('alternative-correct');
        } else if (!data.acertou && alternativaId === data.id_alternativa_selecionada) {
            alt.classList.add('alternative-incorrect-chosen');
        } else if (!data.acertou && ehCorreta) {
            alt.classList.add('alternative-correct');
        }
    });
    
    // Atualizar pontuação
    pontuacaoTotal = data.acertos || 0;
    
    // Atualizar interface se elementos existirem
    const placarElement = document.querySelector('.placar-pontos');
    if (placarElement) {
        placarElement.textContent = pontuacaoTotal;
    }
    
    const questaoAtualElement = document.querySelector('.questao-atual');
    if (questaoAtualElement) {
        questaoAtual = parseInt(questaoAtualElement.textContent) || questaoAtual;
        questaoAtualElement.textContent = questaoAtual + 1;
    }
    
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

// Função para desativar alternativas após resposta
function desativarAlternativas(questaoId) {
    const questaoCard = document.querySelector(`#questao-${questaoId}`);
    if (!questaoCard) return;
    
    const alternativas = questaoCard.querySelectorAll('.alternative');
    alternativas.forEach(alt => {
        alt.style.pointerEvents = 'none';
        alt.style.cursor = 'default';
        alt.style.opacity = '0.7';
    });
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
        
        // Adicionar após o formulário
        const form = questaoCard.querySelector('.questoes-form');
        if (form && form.parentNode) {
            form.parentNode.insertBefore(explicacaoContainer, form.nextSibling);
        }
    }
}

// Event listeners para as alternativas
document.addEventListener('DOMContentLoaded', function() {
    const alternativas = document.querySelectorAll('.alternative');
    const proximaQuestaoBtn = document.querySelector('.next-question-btn');
    const placarPontosSpan = document.querySelector('.placar-pontos');
    const questaoAtualSpan = document.querySelector('.questao-atual');
    const totalQuestoesSpan = document.querySelector('.total-questoes');

    alternativas.forEach(alternativa => {
        alternativa.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const questaoId = this.dataset.questaoId;
            const alternativaId = this.dataset.alternativaId;
            const questaoCard = this.closest('.question-card');
            
            // Verificar se já foi respondida
            if (questaoCard.dataset.respondida === 'true') {
                return;
            }
            
            // Marcar como respondida
            questaoCard.dataset.respondida = 'true';
            
            // Desativar alternativas para evitar cliques duplos
            desativarAlternativas(questaoId);
            
            // Enviar resposta via AJAX
            fetch('/questoes/quiz/validar/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                    id_questao: parseInt(questaoId),
                    id_alternativa: parseInt(alternativaId)
                })
            })
            .then(response => response.json())
                .then(data => {
                if (data.sucesso !== undefined && data.sucesso) {
                    mostrarFeedback(questaoId, data);
                    
                    // Mostrar botão de próxima questão se disponível
                    if (proximaQuestaoBtn) {
                        proximaQuestaoBtn.style.display = 'block';
                    }
                    }
                })
                .catch(error => {
                console.error('Erro na requisição:', error);
                exibirFeedback("Erro ao salvar resposta: " + error.message, false);
            });
        });
    });
    
    // Evento para o botão de próxima questão
    if (proximaQuestaoBtn) {
        proximaQuestaoBtn.addEventListener('click', () => {
            // Verificar se veio de uma questão específica (da lista de questões)
            const urlParams = new URLSearchParams(window.location.search);
            const questaoEspecifica = urlParams.get('questao');
            const idAssunto = urlParams.get('id');
            
            if (questaoEspecifica && idAssunto) {
                // Se veio de uma questão específica, volta para a lista de questões
                const filtroAtivo = localStorage.getItem('filtro_ativo') || 'nao-respondidas';
                window.location.href = `/questoes/assunto/${idAssunto}/?filtro=${filtroAtivo}`;
            } else {
                // Comportamento normal das questões (recarregar para próxima questão)
                window.location.reload();
            }
        });
    }
});

// Função auxiliar para obter cookie
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
