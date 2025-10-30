/**
 * Sistema de Quiz Vertical - Versão Final de Consistência
 * Filtros Dinâmicos com Status Consistente ('certa', 'errada', 'nao-respondida')
 */

// Variáveis globais protegidas contra redeclaração
if (typeof window.pontuacaoTotal === 'undefined') {
    window.pontuacaoTotal = 0;
}

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
    // 1. Marca o card da questão com o novo status (CONSISTENTE: 'certa'/'errada')
    questaoCard.dataset.statusResposta = data.acertou ? 'certa' : 'errada';

    // 2. Atualiza os contadores no filtro
    atualizarContadores();

    // 3. Re-aplica o filtro atual (para esconder/mostrar se necessário)
    const filtroAtual = localStorage.getItem('filtro_ativo') || 'todas';
    aplicarFiltro(filtroAtual);
}

// --- LÓGICA DE FILTRAGEM DINÂMICA ---

// Função que itera sobre todos os cards e aplica o filtro
function aplicarFiltro(filtro) {
    const todosCards = document.querySelectorAll('.question-card');
    
    console.log(`=== APLICANDO FILTRO DINÂMICO: ${filtro} ===`);
    console.log(`Total de cards encontrados: ${todosCards.length}`);
    
    // Salva o filtro no armazenamento local
    localStorage.setItem('filtro_ativo', filtro); 

    let cardsVisiveis = 0;
    let cardsOcultos = 0;

    todosCards.forEach((card, index) => {
        // ✅ CONSISTÊNCIA: Pega o status do atributo de dados com padrão 'nao-respondida'
        const status = card.dataset.statusResposta || 'nao-respondida';
        let deveMostrar = false;

        // ✅ LÓGICA DE FILTRAGEM BASEADA NO FLUXO DINÂMICO (CONSISTENTE)
        switch (filtro) {
            case 'todas':
                deveMostrar = true; // SEMPRE mostra todas
                break;
            case 'respondidas':
                deveMostrar = (status === 'certa' || status === 'errada'); // Questões respondidas
                break;
            case 'nao-respondidas':
                deveMostrar = (status === 'nao-respondida'); // Questões nunca respondidas
                break;
            case 'certas':
                deveMostrar = (status === 'certa'); // Última resposta foi correta
                break;
            case 'erradas':
                deveMostrar = (status === 'errada'); // Última resposta foi incorreta
                break;
        }

        // ✅ APLICAR FILTRO VISUAL COM DISPLAY BLOCK/NONE
        if (deveMostrar) {
            card.style.display = 'block';
            card.style.opacity = '1';
            cardsVisiveis++;
            console.log(`Card ${index + 1} (ID: ${card.dataset.questaoId}): VISÍVEL (Status: ${status})`);
        } else {
            card.style.display = 'none';
            card.style.opacity = '0';
            cardsOcultos++;
            console.log(`Card ${index + 1} (ID: ${card.dataset.questaoId}): OCULTO (Status: ${status})`);
        }
    });
    
    console.log(`=== RESULTADO DO FILTRO ===`);
    console.log(`Cards visíveis: ${cardsVisiveis}`);
    console.log(`Cards ocultos: ${cardsOcultos}`);
    console.log(`Total: ${cardsVisiveis + cardsOcultos}`);
    
    // ✅ ATUALIZA O ESTADO VISUAL DOS BOTÕES DE FILTRO
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filtro === filtro);
    });
    
    console.log(`=== FILTRO "${filtro}" APLICADO COM SUCESSO ===`);
}

// Função auxiliar para recalcular e atualizar os contadores 
function atualizarContadores() {
    const todosCards = document.querySelectorAll('.question-card');
    let contTodas = 0;
    let contRespondidas = 0;
    let contNaoRespondidas = 0;
    let contCertas = 0;
    let contErradas = 0;
    
    console.log('=== ATUALIZANDO CONTADORES DINÂMICOS ===');
    console.log(`Total de cards encontrados: ${todosCards.length}`);
    
    todosCards.forEach((card, index) => {
        // ✅ CONSISTÊNCIA: Pega o status do atributo de dados com padrão 'nao-respondida'
        const status = card.dataset.statusResposta || 'nao-respondida';
        
        contTodas++;
        
        // ✅ LÓGICA DE MIGRAÇÃO: Classificar por status (CONSISTENTE)
        if (status === 'certa' || status === 'errada') {
            contRespondidas++;
        } else {
            contNaoRespondidas++;
        }
        
        if (status === 'certa') {
            contCertas++;
        } else if (status === 'errada') {
            contErradas++;
        }
        
        console.log(`Card ${index + 1} (ID: ${card.dataset.questaoId}): Status = "${status}"`);
    });
    
    // ✅ VERIFICAÇÃO MATEMÁTICA: Todas = Respondidas + Não Respondidas
    const somaRespondidas = contRespondidas + contNaoRespondidas;
    if (contTodas !== somaRespondidas) {
        console.error(`ERRO MATEMÁTICO: Todas (${contTodas}) ≠ Respondidas + Não Respondidas (${somaRespondidas})`);
    }
    
    console.log('=== CONTADORES CALCULADOS ===');
    console.log(`Todas: ${contTodas} (nunca muda)`);
    console.log(`Respondidas: ${contRespondidas} (só aumenta)`);
    console.log(`Não Respondidas: ${contNaoRespondidas} (só diminui)`);
    console.log(`Certas: ${contCertas} (pode aumentar/diminuir)`);
    console.log(`Erradas: ${contErradas} (pode aumentar/diminuir)`);
    
    // ✅ ATUALIZAR ELEMENTOS HTML COM IDs ESPECÍFICOS
    const totalElement = document.querySelector('#contador-total');
    if (totalElement) {
        totalElement.textContent = contTodas;
        console.log(`Contador "Todas" atualizado: ${contTodas}`);
    }
    
    const respondidasElement = document.querySelector('#contador-respondidas');
    if (respondidasElement) {
        respondidasElement.textContent = contRespondidas;
        console.log(`Contador "Respondidas" atualizado: ${contRespondidas}`);
    }

    const naoRespondidasElement = document.querySelector('#contador-nao-respondidas');
    if (naoRespondidasElement) {
        naoRespondidasElement.textContent = contNaoRespondidas;
        console.log(`Contador "Não Respondidas" atualizado: ${contNaoRespondidas}`);
    }
    
    const certasElement = document.querySelector('#contador-certas');
    if (certasElement) {
        certasElement.textContent = contCertas;
        console.log(`Contador "Certas" atualizado: ${contCertas}`);
    }
    
    const erradasElement = document.querySelector('#contador-erradas');
    if (erradasElement) {
        erradasElement.textContent = contErradas;
        console.log(`Contador "Erradas" atualizado: ${contErradas}`);
    }
    
    console.log('=== CONTADORES ATUALIZADOS COM SUCESSO ===');
}

// --- INICIALIZAÇÃO E EVENT LISTENERS ---

// Se estiver na página de Quiz Vertical (usa #questions-container), não executar este script
const __IS_QUIZ_VERTICAL__ = !!document.querySelector('#questions-container');

document.addEventListener('DOMContentLoaded', function () {
  /* Guard desativado para permitir execução também no Quiz Vertical
  if (__IS_QUIZ_VERTICAL__) {
    console.log('quiz.js: ignorado no Quiz Vertical (lógica própria da página).');
    return;
  }
  */

  const alternativas = document.querySelectorAll('.alternative');

  // --- 1. Event Listeners das Alternativas (Lógica AJAX) ---
  alternativas.forEach(alternativa => {
    alternativa.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      const questaoId = this.dataset.questaoId;
      const alternativaId = this.dataset.alternativaId;
      const questaoCard = this.closest('.question-card');

      // Verificar se já foi respondida
      if (questaoCard && questaoCard.dataset.statusResposta) {
        exibirFeedback('Questão já respondida!', false);
        return;
      }

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
        .then(response => {
          if (!response.ok) {
            return response.json().then(data => {
              throw new Error(`Erro ${response.status}: ${data.error || 'Requisição falhou.'}`);
            }).catch(() => {
              throw new Error(`Erro de rede ou servidor: ${response.status}`);
            });
          }
          return response.json();
        })
        .then(data => {
          if (data && data.success) {
            mostrarFeedback(questaoId, data);
          } else if (data && data.error) {
            const card = document.querySelector(`#questao-${questaoId}`);
            if (card) card.dataset.statusResposta = '';
            exibirFeedback(`Erro: ${data.error}`, false);
          }
        })
        .catch(error => {
          console.error('Erro na requisição:', error);
          exibirFeedback(`Erro ao salvar resposta: ${error.message}`, false);
          const card = document.querySelector(`#questao-${questaoId}`);
          if (card) {
            card.dataset.statusResposta = '';
            const alternativasDoCard = card.querySelectorAll('.alternative');
            alternativasDoCard.forEach(alt => {
              alt.style.pointerEvents = 'auto';
              alt.style.cursor = 'pointer';
              alt.style.opacity = '1';
            });
          }
        });
    });
  });

  // --- 2. Restante da inicialização específica desta página (filtros/contadores) ---
  const filtroInicial = localStorage.getItem('filtro_ativo') || 'todas';
  if (typeof aplicarFiltro === 'function') aplicarFiltro(filtroInicial);
  if (typeof atualizarContadores === 'function') atualizarContadores();

  console.log('✅ Sistema de Quiz (template de lista) inicializado');
});