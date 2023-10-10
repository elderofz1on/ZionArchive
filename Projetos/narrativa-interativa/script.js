let choiceHistory = [];
let choiceIdHistory = [];

document.addEventListener("DOMContentLoaded", function () {
    fetch('historia.xml')
        .then(response => response.text())
        .then(data => {
            let parser = new DOMParser();
            let xml = parser.parseFromString(data, "application/xml");
            displayStory(xml);
            displayChoices(xml.querySelector('level1')); // Começamos no Nível 1
        })
        .catch(err => {
            console.error('Erro ao carregar a história:', err);
        });
});

function displayStory(xml) {
    const title = xml.querySelector('story').getAttribute('title');
    const introduction = xml.querySelector('introduction').textContent;

    document.querySelector('h1').textContent = title;
    document.getElementById('introduction').textContent = introduction;
}

function displayChoices(node) {
    const choicesDiv = document.getElementById('choices');
    choicesDiv.innerHTML = ''; // Limpa escolhas anteriores

    const choices = node.querySelectorAll(':scope > choice');
    choices.forEach(choice => {
        const btn = document.createElement('button');
        btn.textContent = choice.getAttribute('description');
        btn.addEventListener('click', () => {
            addChoiceToHistory(btn.textContent);
            addChoiceIdToHistory(choice.getAttribute('id')); // Adiciona o ID da escolha ao histórico

            const nextLevel = choice.querySelector(':scope > level2, :scope > level3, :scope > level4, :scope > level5, :scope > level6, :scope > level7');

            if (nextLevel) {
                choiceHistory.push(node);
                displayChoices(nextLevel);
            }
        });
        choicesDiv.appendChild(btn);
    });

    // Se já fizemos alguma escolha, mostramos o botão para voltar
    if (choiceHistory.length) {
        const backButton = document.createElement('button');
        backButton.textContent = "Voltar";
        backButton.style.backgroundColor = "#dc3545";
        backButton.addEventListener('click', () => {
            removeLastChoiceFromHistory();
            removeLastChoiceIdFromHistory(); // Remove o último ID do histórico
            const previousChoice = choiceHistory.pop();
            displayChoices(previousChoice);
        });
        choicesDiv.appendChild(backButton);
    }
}

function addChoiceToHistory(choice) {
    const li = document.createElement('li');
    li.textContent = choice;
    document.querySelector('#choice-history ul').appendChild(li);
}

function removeLastChoiceFromHistory() {
    const ul = document.querySelector('#choice-history ul');
    if (ul.lastChild) {
        ul.removeChild(ul.lastChild);
    }
}

function addChoiceIdToHistory(choiceId) {
    const li = document.createElement('li');
    li.textContent = choiceId;
    document.querySelector('#choice-id-history ul').appendChild(li);
}

function removeLastChoiceIdFromHistory() {
    const ul = document.querySelector('#choice-id-history ul');
    if (ul.lastChild) {
        ul.removeChild(ul.lastChild);
    }
}
