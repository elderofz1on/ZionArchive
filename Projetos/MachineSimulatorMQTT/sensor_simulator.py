
import os
import pika  # Importa a biblioteca pika para interagir com o RabbitMQ
import time  # Importa a biblioteca time para controlar o tempo de sleep do loop
import socket  # Importa socket para verificar a conectividade com a internet
import json  # Importa json para manipular dados JSON
import random  # Importa random para gerar números aleatórios
import math  # Importa math para realizar operações matemáticas
import xml.etree.ElementTree as ET  # Importa ElementTree para manipular dados XML
import glob  # Importa glob para encontrar todos os caminhos que correspondem a um padrão específico
from datetime import datetime, timedelta  # Importa datetime e timedelta para trabalhar com datas e horas
from dotenv import load_dotenv  # Importa load_dotenv para carregar variáveis de ambiente do arquivo .env

# Carregar variáveis do .env
load_dotenv()
# Obtém as variáveis de ambiente para a URL do RabbitMQ e a chave de roteamento
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
ROUTING_KEY = os.getenv("ROUTING_KEY")

class SensorSimulator:
    def __init__(self, sensor_data):
        """
        Inicializa o simulador com os dados dos sensores fornecidos.
        
        :param sensor_data: dict, dados dos sensores a serem utilizados na simulação.
        """
        self.sensor_data = sensor_data
    
    def generate_value(self, min_val, max_val, mean_val, fluctuation=5):
        """
        Gera um valor flutuante aleatório entre um intervalo especificado.
        
        :param min_val: float, valor mínimo possível.
        :param max_val: float, valor máximo possível.
        :param mean_val: float, valor médio desejado.
        :param fluctuation: float, flutuação permitida em torno do valor médio.
        :return: float, valor aleatório gerado.
        """
        lower_bound = max(min_val, mean_val - fluctuation)
        upper_bound = min(max_val, mean_val + fluctuation)
        return random.uniform(lower_bound, upper_bound)

    def simulate_sensor_failure(self, prob_failure=0.01):
        """
        Simula uma falha no sensor com uma probabilidade especificada.
        
        :param prob_failure: float, probabilidade de falha do sensor.
        :return: bool, True se falhar, False caso contrário.
        """
        return random.random() < prob_failure

    def log_data_to_xml(self, batch_data):
        """
        Loga os dados do sensor em um arquivo XML.
        
        :param batch_data: list, dados do sensor a serem logados.
        """
        date_str = datetime.now().strftime("%Y%m%d")
        log_filename = f"sensor_data_log_{date_str}.xml"
        
        # Verifica se o arquivo de log já existe, se sim, carrega os dados existentes
        if os.path.exists(log_filename):
            tree = ET.parse(log_filename)
            root = tree.getroot()
        else:
            root = ET.Element("SensorDataBatch")
        
        # Adiciona novos dados ao XML
        for data in batch_data:
            sensor_data = ET.SubElement(root, "SensorData")
            for key, value in data.items():
                ET.SubElement(sensor_data, key).text = str(value)
        
        # Salva os dados no arquivo XML
        tree = ET.ElementTree(root)
        with open(log_filename, "wb") as file:
            tree.write(file)
        
        # Limpa logs antigos
        self.clean_old_logs(log_file_prefix="sensor_data_log_", max_logs=7)

    def clean_old_logs(self, log_file_prefix, max_logs):
        """
        Limpa logs antigos, mantendo apenas um número específico de arquivos de log.
        
        :param log_file_prefix: str, prefixo dos arquivos de log.
        :param max_logs: int, número máximo de arquivos de log a serem mantidos.
        """
        log_files = sorted(glob.glob(f"{log_file_prefix}*.xml"))
        for log_file in log_files[:-max_logs]:
            os.remove(log_file)

    def send_to_rabbitmq(self, message):
        """
        Envia uma mensagem para uma fila RabbitMQ.
        
        :param message: str, mensagem a ser enviada.
        """
        # Estabelece conexão com o RabbitMQ e declara a fila
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue=ROUTING_KEY, durable=True)
        
        # Publica a mensagem na fila
        channel.basic_publish(exchange='',
                              routing_key=ROUTING_KEY,
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              ))
        print(f" [x] Enviado '{message}'")
        connection.close()

    def simulate(self):
        """
        Inicia a simulação, gerando dados de sensores, logando-os e enviando-os para a fila RabbitMQ.
        """
        # Aguarda conexão com a internet
        while not self.is_connected():
            print("Aguardando conexão com a internet...")
            time.sleep(5)
        
        specific_sensors = list(self.sensor_data.keys())
        
        # Loop de simulação
        while True:
            batch_data = []
            start_timestamp = datetime.now()
            
            # Gera dados para cada sensor especificado
            for machine_id, sensor_id in specific_sensors:
                faixa_min, faixa_max, valor_medio = self.sensor_data[(machine_id, sensor_id)]
                
                # Adiciona uma pequena variação ao valor médio
                valor_medio += 1 
                valor_medio += 5 * math.sin(start_timestamp.minute / 5)  
                
                # Simula falha no sensor ou gera valor
                if self.simulate_sensor_failure():
                    value = None  
                else:
                    value = self.generate_value(faixa_min, faixa_max, valor_medio)
                
                # Cria timestamp e dados do sensor
                timestamp = start_timestamp + timedelta(minutes=random.randint(0, 5))
                str_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                
                data = {
                    "timestamp": str_timestamp,
                    "CompanyId": "EMPRESA01",
                    "MachineId": machine_id,
                    "SensorId": sensor_id,
                    "Value": value
                }
                
                batch_data.append(data)
                
            # Envia dados para RabbitMQ e loga em XML
            self.send_to_rabbitmq(json.dumps(batch_data))
            self.log_data_to_xml(batch_data)
            
            # Controla o tempo de sleep do loop dependendo do horário
            current_hour = datetime.now().hour
            if 9 <= current_hour <= 17:
                time.sleep(180)  
            else:
                time.sleep(300)  

    @staticmethod
    def is_connected():
        """
        Verifica se há conexão com a internet.
        
        :return: bool, True se conectado, False caso contrário.
        """
        try:
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            pass
        return False


# Dados dos sensores
sensor_data = {
    ("M01", "S01"): (70, 100, 80),
    ("M01", "S02"): (500, 900, 700),
    ("M02", "S03"): (100, 140, 120),
    ("M03", "S04"): (500, 900, 700),
    ("M04", "S05"): (160, 210, 170),
    ("M05", "S06"): (70, 100, 80),
    ("M05", "S07"): (100, 140, 130),
    ("M06", "S08"): (7000, 12000, 10800),
    ("M06", "S09"): (100, 140, 130),
    ("M07", "S10"): (70, 100, 80),
    ("M07", "S11"): (7000, 12000, 10800),
    ("M07", "S16"): (100, 400, 201),
    ("M08", "S12"): (70, 100, 80),
    ("M08", "S13"): (1000, 3000, 2000),
    ("M09", "S14"): (1500, 1900, 1765),
    ("M10", "S15"): (1500, 1900, 1765)
}

# Inicia a simulação
simulator = SensorSimulator(sensor_data)
simulator.simulate()
