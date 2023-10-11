import machine
import socket
import network
import uhashlib
import ubinascii
import ubluetooth

# Configurações do dispositivo
LED_PIN = 12
MANUFACTURER = "ESP32-SmartLock"
MODEL = "SSL01"
DEVICE_ID = "BE4ADCD4-E8FA-40B0-ACB5-2B2B25B5B9"
ESSID = "ESP32-SmartLock-06"
WIFI_PASS = "12345678"
DEFAULT_TOKEN = "ACB5"
TOKEN_FILE = "token.txt"
SECRET_KEY = "minhachave"

led = machine.Pin(LED_PIN, machine.Pin.OUT)

class BLEHandler():
    def __init__(self, name):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def ble_irq(self, event, data):
        if event == 3:  # An event indicating a BLE message received
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            print("Received message:", message)
            self.handle_message(message)

    def register(self):
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
        
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
        
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytearray(b'\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)

    def handle_message(self, message):
        if message == "on":
            led.value(0)
        elif message == "off":
            led.value(1)

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

def main():
    init_wifi()
    ble_handler = BLEHandler("ESP32-SmartLock-BLE")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        # Lida com solicitações WiFi
        conn, addr = s.accept()
        request = conn.recv(1024).decode("utf-8")
        action, response = handle_request(request)
        if action == "redirect":
            conn.send('HTTP/1.1 302 Found\r\nLocation: /\r\n\r\n')
        else:
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            conn.send(response)
        conn.close()

        # Lida com solicitações BLE
        # Nota: A implementação exata dependerá da sua lógica de negócios e da biblioteca BLE.
        # Você pode precisar ajustar o código para se adequar às suas necessidades específicas.
        # Aqui, estamos assumindo que você implementará a lógica necessária para obter dados do BLE
        # na função ble_irq da classe BLEHandler.

if __name__ == "__main__":
    main()
