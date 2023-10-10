// Adiciona um tooltip ao passar o mouse sobre um elemento com ID
function addTooltip(elementId, helpText) {
  const element = document.getElementById(elementId);
  if (element) {
    element.addEventListener('mouseover', function() {
      const tooltip = document.createElement('div');
      tooltip.innerText = helpText;
      tooltip.className = 'custom-help-tooltip';
      document.body.appendChild(tooltip);
      tooltip.style.top = `${element.getBoundingClientRect().bottom + window.scrollY}px`;
      tooltip.style.left = `${element.getBoundingClientRect().left + window.scrollX}px`;
      
      // Remove o tooltip quando o mouse sai do elemento
      element.addEventListener('mouseout', function() {
        document.body.removeChild(tooltip);
      });
    });
  }
}

// Adiciona estilos para o tooltip na página web
const tooltipStyles = `
.custom-help-tooltip {
  position: absolute;
  background-color: #f9f9f9;
  color: #333;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  z-index: 1000;
}`;

const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = tooltipStyles;
document.head.appendChild(styleSheet);

// Ouve mensagens enviadas do popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // Verifica se a mensagem é "get_help"
  if (message.message === "get_help") {
    // Exemplo: Adiciona um tooltip ao elemento com ID 'loginButton'
    addTooltip('loginButton', 'Clique aqui para fazer login.');
  }
  // Verifica se a mensagem é "get_ids"
  else if (message.message === "get_ids") {
    // Coleta todos os IDs da página
    let idsOnPage = [];
    document.querySelectorAll('[id]').forEach((element) => {
      idsOnPage.push(element.id);
    });
    // Envia os IDs coletados para o popup
    chrome.runtime.sendMessage({type: "ID_LIST", ids: idsOnPage});
  }
});
