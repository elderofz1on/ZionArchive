chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "ID_LIST") {
    correlateIdsWithHelpMessages(message.ids);
  }
});

function correlateIdsWithHelpMessages(ids) {
  const helpData = {
    "helpMessages": {
      "loginButton": "Clique aqui para fazer login.",
      "signupButton": "Clique aqui para criar uma nova conta.",
      "passwordInput": "Digite sua senha segura aqui."
    }
  };

  ids.forEach(id => {
    if (helpData.helpMessages[id]) {
      console.log(`Ajuda para ${id}: ${helpData.helpMessages[id]}`);
      // Você pode armazenar essas correspondências ou enviá-las diretamente para o popup ou content script.
    } else {
      console.log(`Sem mensagem de ajuda para ${id}`);
    }
  });
}
