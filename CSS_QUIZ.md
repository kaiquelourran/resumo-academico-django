# CSS Global - Estilos do Sistema de Quiz

Este arquivo documenta os estilos CSS globais que replicam a funcionalidade do arquivo PHP `quiz.css`.

## Arquivos CSS

### `static/css/global.css`
Arquivo principal com todos os estilos globais do sistema de quiz, incluindo:
- Reset básico
- Estilos de header e footer
- Cards e botões
- Formulários
- Tabelas
- Estilos específicos do quiz (filtros, questões, alternativas)
- Animações e feedback visual
- Classes utilitárias

## Estrutura dos Estilos

### 1. Reset e Base
```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Arial', sans-serif; }
```

### 2. Header Fixo
```css
header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    position: fixed;
    top: 0;
    z-index: 1000;
}
```

### 3. Cards
```css
.card {
    background: white;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}
```

### 4. Botões
```css
.btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 25px;
    transition: all 0.3s ease;
}
```

### 5. Quiz Styles
- `.container` - Container principal com gradiente roxo
- `.filtros-container` - Container dos filtros
- `.filtros-grid` - Grid de botões de filtro
- `.filtro-btn` - Botão individual de filtro
- `.question-card` - Card da questão
- `.alternativa` - Alternativa clicável
- `.alternativa-correta` - Feedback verde
- `.alternativa-incorreta` - Feedback vermelho

### 6. Animações
```css
@keyframes pulseGreen { /* Animação para resposta correta */ }
@keyframes pulseRed { /* Animação para resposta incorreta */ }
@keyframes fadeIn { /* Animação de aparecimento */ }
```

## Uso no Django

### No Template Base
```html
<link rel="stylesheet" href="{% static 'css/global.css' %}">
```

### Classes Disponíveis

#### Botões
- `.btn` - Botão padrão
- `.btn-primary` - Botão primário
- `.btn-outline` - Botão outline
- `.btn:hover` - Hover no botão

#### Cards
- `.card` - Card padrão
- `.card:hover` - Hover no card
- `.question-card` - Card de questão

#### Alternativas
- `.alternativa` - Alternativa padrão
- `.alternativa:hover` - Hover na alternativa
- `.alternativa.selecionada` - Alternativa selecionada
- `.alternativa-correta` - Feedback de correto
- `.alternativa-incorreta` - Feedback de incorreto

#### Alertas
- `.alert` - Alert padrão
- `.alert-success` - Alert de sucesso (verde)
- `.alert-danger` - Alert de erro (vermelho)
- `.alert-warning` - Alert de aviso (amarelo)
- `.alert-info` - Alert de informação (azul)

#### Utility Classes
- `.text-center` - Texto centralizado
- `.mt-3` - Margin top
- `.mb-3` - Margin bottom
- `.p-3` - Padding

## Responsividade

O CSS é totalmente responsivo com media queries para:
- **Desktop**: Estilos completos
- **Tablet** (até 768px): Ajustes de layout
- **Mobile** (< 768px): Layout em coluna única

### Media Query Principal
```css
@media (max-width: 768px) {
    /* Estilos para mobile */
}
```

## Personalização

### Cores do Gradiente
Altere as cores do gradiente roxo padrão:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Tamanho dos Cards
```css
.card { padding: 2rem; /* Ajustar conforme necessário */ }
```

### Animações
```css
/* Ajustar velocidade das animações */
transition: all 0.3s ease; /* 0.3s = velocidade atual */
```

## Comparação PHP → Django

| PHP (`quiz.css`) | Django (`global.css`) |
|------------------|------------------------|
| Estilos inline ou separados | CSS modularizado |
| `background: linear-gradient(...)` | Mesmo código CSS |
| Animações via CSS | Mesmo código CSS |
| Responsive via media queries | Mesmo código CSS |

## Dependências

Nenhuma dependência adicional. O CSS usa apenas recursos nativos do navegador.

## Browser Support

- ✅ Chrome/Edge (últimas 2 versões)
- ✅ Firefox (últimas 2 versões)
- ✅ Safari (últimas 2 versões)
- ✅ Opera (últimas 2 versões)
- ✅ Mobile browsers

## Notas Importantes

1. **Reset CSS**: O reset básico (* { margin: 0; padding: 0; }) garante compatibilidade entre navegadores
2. **Box-sizing**: Sempre use `box-sizing: border-box` para cálculos de largura/altura corretos
3. **Transitions**: Todas as interações têm transition de 0.3s para UX suave
4. **Shadows**: Box-shadow cria profundidade visual
5. **Gradient**: Use gradientes para um visual moderno

## Troubleshooting

### Estilos não aplicados?
- Verifique se o arquivo foi carregado: `{% static 'css/global.css' %}`
- Limpe o cache do navegador (Ctrl+Shift+R)
- Verifique a ordem de importação dos CSS

### Layout quebrado em mobile?
- Verifique as media queries
- Teste diferentes tamanhos de tela
- Use ferramentas de desenvolvedor do navegador

### Animações não funcionam?
- Verifique se o elemento tem a classe correta
- Verifique se há conflito com outros CSS
- Use `!important` apenas se necessário

