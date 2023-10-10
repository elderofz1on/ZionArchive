import machine
import socket
import network

# Configura o LED
led = machine.Pin(2, machine.Pin.OUT)

# Token de segurança
TOKEN_SECRET = "asdf"

# Inicializa e configura o ponto de acesso WiFi no ESP32
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP32-SmartLock-Controller", password="12345678")

print('Rede criada. Conecte-se a "ESP32-SmartLock-Controller" com a senha "12345678".')

# Função para controlar o LED e retornar a página HTTP
def handle_request(request):
    # Verifica se é POST e controla o LED
    if "POST /" in request:
        # Verificar se o token está correto
        if TOKEN_SECRET in request:
            if "led=on" in request:
                led.value(0)
            elif "led=off" in request:
                led.value(1)
        
    # Página HTML para controlar o LED
    html = """
    <html>
    <head>
        <title>ESP32 SmartLock Controller 04</title>
        <style>
            button {
                font-size: 30px;
                margin: 10px;
                cursor: pointer;
                width: 400px;
                height: 100px;
            }
            
            .green {
                background-color: green;
                color: white;
            }

            .red {
                background-color: red;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>ESP32 SmartLock Controller 04</h1><br>
        <form action="/" method="post">
            <input type="text" name="token" placeholder="Security token" required><br><br>
            <button class="green" name="led" value="on">Ligar LED  </button>
        </form>
        <form action="/" method="post">
            <input type="text" name="token" placeholder="Security token" required><br><br>
            <button class="red" name="led" value="off">Desligar LED</button>
        </form>
    </body>
    </html>
    """
    return html

# Cria um servidor socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    response = handle_request(request)
    conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
    conn.send(response)
    conn.close()


