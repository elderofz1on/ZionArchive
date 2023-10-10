import machine
import socket
import network
import uos
import uhashlib
import ubinascii

# Configurações do dispositivo
LED_PIN = 2
ESSID = "ESP32-SmartLock-Controller"
WIFI_PASS = "12345678"
DEFAULT_TOKEN = "ACB5"
TOKEN_FILE = "token.txt"
SECRET_KEY = "minhachave"

led = machine.Pin(LED_PIN, machine.Pin.OUT)

def hash_token(token):
    """Retorna o hash SHA256 do token."""
    h = uhashlib.sha256()
    h.update(token + SECRET_KEY)
    return ubinascii.hexlify(h.digest()).decode()

def load_token():
    """Carrega o token do arquivo. Se não existir, retorna o token default."""
    try:
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    except OSError:
        return hash_token(DEFAULT_TOKEN)

def update_token(new_token):
    """Atualiza o token no arquivo."""
    hashed_token = hash_token(new_token)
    with open(TOKEN_FILE, 'w') as f:
        f.write(hashed_token)

def init_wifi():
    """Configura e inicializa o ponto de acesso WiFi."""
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ESSID, password=WIFI_PASS)
    print(f'Rede criada. Conecte-se a "{ESSID}" com a senha "{WIFI_PASS}".')

def handle_request(request):
    """Trata as requisições e controla o LED."""
    stored_token = load_token()

    # Verificar atualização de token
    if "POST /update_token" in request:
        start_idx = request.find("new_token=") + len("new_token=")
        end_idx = request.find("&", start_idx)
        new_token = request[start_idx:end_idx]
        update_token(new_token)
        return "redirect", "Token updated successfully!"

    # Verificar se o token está correto
    if "POST /" in request:
        start_idx = request.find("token=") + len("token=")
        end_idx = request.find("&", start_idx)
        provided_token = request[start_idx:end_idx]
        if hash_token(provided_token) == stored_token:
            print(f'a')
            if "led=on" in request:
                led.value(0)
            elif "led=off" in request:
                led.value(1)
            return "redirect", "LED command processed!"
        else:
            print(f'b')
            return "redirect", "Unauthorized request!"

    return "content", generate_html_page()

def generate_html_page():
    """Gera a página HTML."""
    html = """
    <html>
    <head>
        <title>ESP32 SmartLock Controller 05</title>
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
        <h1>ESP32 SmartLock Controller 05</h1><br>
        <form action="/" method="post">
            <input type="text" name="token" placeholder="Security token" required><br><br>
            <button class="green" name="led" value="on">Ligar LED</button>
        </form>
        <form action="/" method="post">
            <input type="text" name="token" placeholder="Security token" required><br><br>
            <button class="red" name="led" value="off">Desligar LED</button>
        </form>
        <form action="/update_token" method="post">
            <input type="text" name="new_token" placeholder="New token" required><br><br>
            <button type="submit">Update Token</button>
        </form>
    </body>
    </html>
    """
    return html

def main():
    """Ponto de entrada principal."""
    init_wifi()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024).decode("utf-8")
        action, response = handle_request(request)
        if action == "redirect":
            conn.send('HTTP/1.1 302 Found\r\nLocation: /\r\n\r\n')
        else: # action == "content"
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            conn.send(response)
        conn.close()

# Executa o programa
if __name__ == "__main__":
    main()
