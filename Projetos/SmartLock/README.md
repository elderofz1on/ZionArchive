# README.md

## ESP32-SmartLock

### Descrição do Projeto

O projeto **ESP32-SmartLock** é um sistema de controle de fechadura inteligente desenvolvido para o microcontrolador ESP32. Utiliza tanto a tecnologia Wi-Fi quanto Bluetooth Low Energy (BLE) para interagir com o usuário, permitindo o controle de um LED (simulando uma fechadura) e a atualização de um token de segurança.

### Funcionalidades

1. **Controle de LED via Wi-Fi:**
   - Criação de uma rede Wi-Fi para permitir a interação com o dispositivo.
   - Interface web para controlar o estado do LED (ligado/desligado) e atualizar o token de segurança.

2. **Controle via Bluetooth:**
   - Utiliza BLE para permitir a conexão de dispositivos móveis.
   - Possibilidade de expansão para controle do LED ou outras funcionalidades via BLE.

3. **Segurança:**
   - Utiliza tokens para autenticação das requisições HTTP.
   - Permite a atualização do token de segurança via interface web.

### Como Usar

#### Conexão Wi-Fi

1. Conecte-se à rede Wi-Fi criada pelo dispositivo, utilizando as credenciais abaixo:
   - **SSID:** ESP32-SmartLock-06
   - **Senha:** 12345678

2. Acesse a interface web através de um navegador e utilize o token de segurança para interagir com o dispositivo.

#### Conexão Bluetooth

1. Ative o Bluetooth em seu dispositivo móvel e procure pelo dispositivo "ESP32-SmartLock".
2. Conecte-se e utilize as funcionalidades disponíveis (a serem implementadas em futuras versões).

### Estrutura do Código

O código está estruturado nas seguintes funções principais:

- `hash_token(token)`: Gera um hash SHA-256 do token fornecido concatenado com uma chave secreta.
- `load_token()`: Carrega o token de segurança armazenado no sistema de arquivos do dispositivo.
- `update_token(new_token)`: Atualiza o token de segurança armazenado.
- `init_wifi()`: Inicializa a funcionalidade Wi-Fi, criando uma rede para interação com o usuário.
- `handle_request(request)`: Lida com as requisições HTTP recebidas, controlando o LED e atualizando o token conforme necessário.
- `generate_html_page()`: Gera a página HTML para a interface web do dispositivo.
- `init_ble()`: Inicializa a funcionalidade Bluetooth Low Energy (BLE) e define os serviços e características.
- `main()`: Função principal que inicializa o Wi-Fi e o BLE, e entra em um loop para lidar com as requisições HTTP.
