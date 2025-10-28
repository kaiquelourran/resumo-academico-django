document.addEventListener('DOMContentLoaded', () => {
    const questoesForm = document.querySelector('form');
    const proximaQuestaoBtn = document.querySelector('.next-question-btn');
    const placarPontosSpan = document.querySelector('.placar-pontos');
    const questaoAtualSpan = document.querySelector('.questao-atual');
    const totalQuestoesSpan = document.querySelector('.total-questoes');


    if (questoesForm) {
        questoesForm.addEventListener('click', (event) => {
            if (event.target.tagName === 'INPUT' && event.target.type === 'radio') {
                const alternativaSelecionada = event.target;
                const respostaId = alternativaSelecionada.value;
                const idQuestao = alternativaSelecionada.closest('.questoes-form').dataset.idQuestao;
                const alternativaCorretaElement = questoesForm.querySelector('[data-correta="true"]');
                const alternativaCorretaId = alternativaCorretaElement ? alternativaCorretaElement.dataset.alternativeId : null;
                
                // Verifica se a resposta está correta
                const respostaCorreta = respostaId === alternativaCorretaId;

                // Envia a resposta para o servidor
                fetch('processar_resposta.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        id_questao: idQuestao,
                        id_alternativa: respostaId,
                        resposta: respostaId,
                        usuario: 'anonimo',
                        acertou: respostaCorreta ? 1 : 0
                    })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Requisição inválida');
                    }
                    return response.json();
                })
                .then(data => {
                    // Atualiza a pontuação na tela com base na resposta do servidor
                    if (data.sucesso) {
                        if (placarPontosSpan) placarPontosSpan.textContent = data.acertos;
                        
                        // Atualiza o número da questão atual
                        if (questaoAtualSpan && totalQuestoesSpan) {
                            const questaoAtualNum = parseInt(questaoAtualSpan.textContent);
                            const totalQuestoes = parseInt(totalQuestoesSpan.textContent);
                            
                            if (questaoAtualNum < totalQuestoes) {
                                questaoAtualSpan.textContent = questaoAtualNum + 1;
                            }
                        }
                        
                        if (respostaCorreta) {
                            if (typeof exibirFeedback === 'function') exibirFeedback("Correto! 😄", true);
                        } else {
                            if (typeof exibirFeedback === 'function') exibirFeedback("Incorreto! 😥", false);
                        }
                    } else {
                        console.error('Erro ao salvar resposta:', data.erro);
                        if (typeof exibirFeedback === 'function') exibirFeedback("Erro ao salvar a resposta.", false);
                    }
                })
                .catch(error => {
                    console.error('Erro de requisição:', error);
                    if (typeof exibirFeedback === 'function') exibirFeedback("Erro ao salvar resposta: " + error.message, false);
                });

                // Desativa as alternativas e mostra o botão "Próxima Questão"
                if (typeof desativarAlternativas === 'function') desativarAlternativas();
                if (proximaQuestaoBtn) proximaQuestaoBtn.style.display = 'block';
            }
        });
    }
    
    // Evento para o botão de próxima questão
    if (proximaQuestaoBtn) {
        proximaQuestaoBtn.addEventListener('click', () => {
            // Verifica se veio de uma questão específica (da lista de questões)
            const urlParams = new URLSearchParams(window.location.search);
            const questaoEspecifica = urlParams.get('questao');
            const idAssunto = urlParams.get('id');
            
            if (questaoEspecifica && idAssunto) {
                // Se veio de uma questão específica, volta para a lista de questões
                // mantendo o filtro ativo
                const filtroAtivo = localStorage.getItem('filtro_ativo') || 'nao-respondidas';
                window.location.href = `listar_questoes.php?id=${idAssunto}&filtro=${filtroAtivo}`;
            } else {
                // Comportamento normal das questões (recarregar para próxima questão aleatória)
                window.location.reload();
            }
        });
    }
});

