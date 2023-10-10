# 4Help Extension

## Descrição

A extensão 4Help para Google Chrome foi criada com o objetivo de demonstrar a construção de um projeto para auxiliar usuários, fornecendo tooltips informativas e coletando IDs de elementos HTML em páginas da web. A extensão oferece uma interface de popup que permite aos usuários solicitar ajuda (na forma de tooltips) ou obter uma lista de todos os IDs de elementos na página web ativa.

## Funcionalidades

- **Get Help**: Ao clicar neste botão, tooltips são exibidas na página da web ativa para auxiliar o usuário.
- **Get IDs**: Este botão, quando clicado, recupera todos os IDs de elementos da página web ativa e os exibe na interface do popup da extensão.

## Estrutura do Projeto

O projeto está estruturado nos seguintes arquivos:

- `4help.html`: Arquivo HTML que define a UI do popup da extensão.
- `4help.js`: Script que gerencia a interação do usuário com o popup e comunica com o script de conteúdo.
- `background.js`: Script de background que lida com mensagens e correlaciona IDs com mensagens de ajuda.
- `contentScript.js`: Script de conteúdo que interage com a página da web e lida com mensagens do popup.
- `styles.css`: Folha de estilo CSS que define a aparência da UI do popup.
- `manifest.json`: (Nota: Este arquivo precisa ser criado/corrigido) Arquivo de manifesto que contém metadados sobre a extensão.

## Como Usar

### Instalação

1. Faça o clone do repositório para o seu computador.
2. Abra o Google Chrome e navegue até `chrome://extensions/`.
3. Ative o modo "Developer mode" (Modo do desenvolvedor).
4. Clique em "Load unpacked" (Carregar sem compactação) e selecione a pasta do projeto.
5. A extensão agora deve estar visível na barra de ferramentas do Chrome.

### Uso Básico

- Clique no ícone da extensão 4Help na barra de ferramentas do Chrome para abrir o popup.
- **Para obter ajuda**: Clique no botão "Get Help". Tooltips informativas serão exibidas na página da web ativa.
- **Para obter IDs**: Clique no botão "Get IDs". Uma lista de todos os IDs de elementos na página web ativa será exibida no popup.

## Contribuindo

### Reportando Bugs

Use a seção de "Issues" do GitHub para reportar bugs. Certifique-se de descrever o bug e os passos para reproduzi-lo de forma clara.

### Sugerindo Melhorias

Sugestões e pedidos de melhorias também podem ser feitos através da seção de "Issues" do GitHub.

### Desenvolvimento

1. Faça o fork do projeto.
2. Crie uma nova branch para suas alterações.
3. Faça suas alterações ou adições.
4. Faça um pull request detalhando suas alterações.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.

---

**Nota**: Certifique-se de revisar e ajustar conforme necessário, especialmente a seção de "Licença" e adicionar o arquivo `LICENSE.md` correspondente ao seu projeto.
