import machine
import socket
import network
import uhashlib
import ubinascii
import bluetooth

# Configurações do dispositivo
LED_PIN = 2
MANUFACTURER = "ESP32-SmartLock"
MODEL = "SSL01"
DEVICE_ID = "BE4ADCD4-E8FA-40B0-ACB5-2B2B25B5B9"
ESSID = "ESP32-SmartLock-06"
WIFI_PASS = "12345678"
DEFAULT_TOKEN = "ACB5"
TOKEN_FILE = "token.txt"
SECRET_KEY = "minhachave"

led = machine.Pin(LED_PIN, machine.Pin.OUT)

def hash_token(token):
    h = uhashlib.sha256()
    h.update(token + SECRET_KEY)
    return ubinascii.hexlify(h.digest()).decode()

def load_token():
    try:
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    except OSError:
        return hash_token(DEFAULT_TOKEN)

def update_token(new_token):
    hashed_token = hash_token(new_token)
    with open(TOKEN_FILE, 'w') as f:
        f.write(hashed_token)

def init_wifi():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ESSID, password=WIFI_PASS)
    print(f'Rede criada. Conecte-se a "{ESSID}" com a senha "{WIFI_PASS}".')

def handle_request(request):
    stored_token = load_token()

    if "POST /update_token" in request:
        start_idx = request.find("new_token=") + len("new_token=")
        end_idx = request.find("&", start_idx)
        new_token = request[start_idx:end_idx]
        update_token(new_token)
        return "redirect", "Token updated successfully!"

    if "POST /" in request:
        start_idx = request.find("token=") + len("token=")
        end_idx = request.find("&", start_idx)
        provided_token = request[start_idx:end_idx]
        if hash_token(provided_token) == stored_token:
            if "led=on" in request:
                led.value(0)
            elif "led=off" in request:
                led.value(1)
            return "redirect", "LED command processed!"
        else:
            return "redirect", "Unauthorized request!"

    return "content", generate_html_page()

def generate_html_page():
    device_info = f"""
        Manufacturer: {MANUFACTURER}<br>
        Model: {MODEL}<br>
        Device ID: {DEVICE_ID}
    """
    html = f"""
    <html>
    <head>
        <title>{ESSID}</title>
        <style>
            button {{
                font-size: 30px;
                margin: 10px;
                cursor: pointer;
                width: 300px;
                height: 70px;
            }}
            .green {{
                background-color: green;
                color: white;
            }}
            .red {{
                background-color: red;
                color: white;
            }}
        </style>
    </head>
    <body>
        <h1>{ESSID}</h1><br>
        <p><strong>Device Info:</strong></p>
        <p>{device_info}</p><br>   
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

def init_ble():
    ble = bluetooth.BLE()
    ble.active(True)

    SERVICE_UUID = bluetooth.UUID('E625601E-9E55-4597-A598-76018A0D293D')
    CHAR_UUID = bluetooth.UUID('ADAFD546-3D1D-4F1F-9CBE-BE291F351A1B')

    srv = ble.service(uuid=SERVICE_UUID, isprimary=True)
    char = srv.characteristic(uuid=CHAR_UUID, value=5)
    char_desc = char.descriptor(uuid=bluetooth.UUID('2901'), value='LED control')

    def ble_irq(event, data):
        if event == 1:  # Conexão BLE estabelecida
            print("Device connected")
        elif event == 2:  # Conexão BLE desconectada
            print("Device disconnected")
        elif event == 3:  # Solicitação de escrita BLE
            print("Data received:", data)
            # Aqui você pode adicionar código para lidar com os dados recebidos
            # Por exemplo, ligar/desligar o LED com base nos dados recebidos

    ble.irq(ble_irq)
    ble.advertise(name='ESP32-SmartLock', services=[srv])

def main():
    init_wifi()
    init_ble()  # Inicializa o BLE

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024).decode("utf-8")
        action, response = handle_request(request)
        if action == "redirect":
            conn.send('HTTP/1.1 302 Found\r\nLocation: /\r\n\r\n')
        else:
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            conn.send(response)
        conn.close()

if __name__ == "__main__":
    main()
