// Adiciona um ouvinte de evento ao botão "Get Help"
document.getElementById('getHelp').addEventListener('click', function() {
  // Query para a aba ativa na janela atual
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    const activeTab = tabs[0];
    // Envia uma mensagem para o script de conteúdo na aba ativa
    chrome.tabs.sendMessage(activeTab.id, {"message": "get_help"});
  });
});

// Adiciona um ouvinte de evento ao botão "Get IDs"
document.getElementById('getIds').addEventListener('click', function() {
  // Query para a aba ativa na janela atual
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    const activeTab = tabs[0];
    // Envia uma mensagem para o script de conteúdo na aba ativa
    chrome.tabs.sendMessage(activeTab.id, {"message": "get_ids"});
  });
});

// Ouve mensagens enviadas do script de conteúdo
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // Verifica se a mensagem é do tipo "ID_LIST"
  if (message.type === "ID_LIST") {
    // Obtém o elemento que exibirá a lista de IDs
    const idListElement = document.getElementById('idList');
    // Limpa IDs anteriores
    idListElement.innerHTML = "";
    // Itera sobre os IDs recebidos
    message.ids.forEach(id => {
      // Cria um novo item de lista para cada ID
      const listItem = document.createElement('li');
      // Define o texto do item da lista como o ID
      listItem.textContent = id;
      // Adiciona o item da lista ao elemento da lista
      idListElement.appendChild(listItem);
    });
  }
});
