from machine import Pin
from time import sleep

# Teclado Matricial
class Keypad():
    def __init__(self, rowPins, colPins, keys):
        self.rowPins = [Pin(pin, Pin.OUT) for pin in rowPins]
        self.colPins = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in colPins]
        self.keys = keys
        for pin in self.rowPins:
            pin.value(1)

    def getKey(self):
        for rowIndex, rowPin in enumerate(self.rowPins):
            rowPin.value(0)
            for colIndex, colPin in enumerate(self.colPins):
                if colPin.value() == 0:
                    key = self.keys[rowIndex][colIndex]
                    rowPin.value(1)
                    return key
            rowPin.value(1)
        return None

# Definições do teclado e relé
RELAY_PIN = Pin(19, Pin.OUT)
ROW_PINS = [12, 14, 27, 26]
COL_PINS = [25, 33, 32]
KEYS = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

keypad = Keypad(ROW_PINS, COL_PINS, KEYS)
manufacturer = "SenaiSmartLocker"
model = "SSL01"
device_ID = "BE4ADCD4-E8FA-40B0-ACB5-2B2B25B5B9"
password_1 = "6666" # admin
password_2 = "4444"
password_3 = "5555"
input_password = ""

RELAY_PIN.value(0)  # bloquear fechadura

while True:
    key = keypad.getKey()
    if key:
        print(key)
        if key == '*':
            input_password = ""
        elif key == '#':
            if input_password in [password_1, password_2, password_3]:
                print("Senha valida | desbloquear fechadura")
                RELAY_PIN.value(1)  # desbloquear fechadura
                sleep(5)  # aguarda x segundos 
                RELAY_PIN.value(0)  # bloquear fechadura
            else:
                print("Senha invalida | Tente novamente")
            input_password = ""
        else:
            input_password += key
        sleep(0.2)  # delay
