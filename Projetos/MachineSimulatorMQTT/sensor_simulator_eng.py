
import os
import pika  # Used for RabbitMQ message queueing
import time  # Used for time.sleep function
import socket  # Used to check internet connection
import json  # Used to convert Python dict to JSON string
import random  # Used to generate random numbers
import math  # Used for mathematical operations
import xml.etree.ElementTree as ET  # Used for XML file operations
import glob  # Used to find all the pathnames matching a specified pattern
from datetime import datetime, timedelta  # Used for date and time operations
from dotenv import load_dotenv  # Used to load variables from .env file

# Load environment variables from .env file
load_dotenv()
RABBITMQ_URL = os.getenv("RABBITMQ_URL")  # URL for RabbitMQ
ROUTING_KEY = os.getenv("ROUTING_KEY")  # Routing key for RabbitMQ

class SensorSimulator:
    def __init__(self, sensor_data):
        """
        Initialize the SensorSimulator with provided sensor data.
        
        :param sensor_data: dict, sensor data to be used in the simulation
        """
        self.sensor_data = sensor_data
    
    def generate_value(self, min_val, max_val, mean_val, fluctuation=5):
        """
        Generate a random float value within a specified range.
        
        :param min_val: float, minimum possible value
        :param max_val: float, maximum possible value
        :param mean_val: float, desired mean value
        :param fluctuation: float, allowed fluctuation around the mean value
        :return: float, generated random value
        """
        lower_bound = max(min_val, mean_val - fluctuation)
        upper_bound = min(max_val, mean_val + fluctuation)
        return random.uniform(lower_bound, upper_bound)

    def simulate_sensor_failure(self, prob_failure=0.01):
        """
        Simulate a sensor failure with a specified probability.
        
        :param prob_failure: float, probability of sensor failure
        :return: bool, whether the sensor fails or not
        """
        return random.random() < prob_failure

    def log_data_to_xml(self, batch_data):
        """
        Log sensor data to an XML file.
        
        :param batch_data: list of dict, sensor data to be logged
        """
        date_str = datetime.now().strftime("%Y%m%d")
        log_filename = f"sensor_data_log_{date_str}.xml"
        
        # Check if log file for the current date exists, if not create a new root
        if os.path.exists(log_filename):
            tree = ET.parse(log_filename)
            root = tree.getroot()
        else:
            root = ET.Element("SensorDataBatch")
        
        # Append new sensor data to the XML
        for data in batch_data:
            sensor_data = ET.SubElement(root, "SensorData")
            for key, value in data.items():
                ET.SubElement(sensor_data, key).text = str(value)
        
        # Write the updated XML data back to the file
        tree = ET.ElementTree(root)
        with open(log_filename, "wb") as file:
            tree.write(file)
        
        # Clean old logs
        self.clean_old_logs(log_file_prefix="sensor_data_log_", max_logs=7)

    def clean_old_logs(self, log_file_prefix, max_logs):
        """
        Clean old log files, keeping only a specified number of log files.
        
        :param log_file_prefix: str, prefix of the log files
        :param max_logs: int, maximum number of log files to keep
        """
        log_files = sorted(glob.glob(f"{log_file_prefix}*.xml"))
        for log_file in log_files[:-max_logs]:
            os.remove(log_file)

    def send_to_rabbitmq(self, message):
        """
        Send a message to a RabbitMQ queue.
        
        :param message: str, message to be sent
        """
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue=ROUTING_KEY, durable=True)
        
        # Publish the message to RabbitMQ
        channel.basic_publish(exchange='',
                              routing_key=ROUTING_KEY,
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              ))
        print(f" [x] Sent '{message}'")
        connection.close()

    def simulate(self):
        """
        Start the simulation, generating sensor data, logging it, and sending it to RabbitMQ.
        """
        # Wait for an internet connection before starting the simulation
        while not self.is_connected():
            print("Waiting for an internet connection...")
            time.sleep(5)
        
        specific_sensors = list(self.sensor_data.keys())
        
        # Main simulation loop
        while True:
            batch_data = []
            start_timestamp = datetime.now()
            
            # Generate sensor data
            for machine_id, sensor_id in specific_sensors:
                min_val, max_val, mean_val = self.sensor_data[(machine_id, sensor_id)]
                
                # Modify mean value over time
                mean_val += 1 
                mean_val += 5 * math.sin(start_timestamp.minute / 5)  
                
                # Simulate sensor value or failure
                if self.simulate_sensor_failure():
                    value = None  
                else:
                    value = self.generate_value(min_val, max_val, mean_val)
                
                # Create a timestamp for the generated data
                timestamp = start_timestamp + timedelta(minutes=random.randint(0, 5))
                str_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                
                # Append the generated data to the batch
                data = {
                    "timestamp": str_timestamp,
                    "CompanyId": "COMPANY01",
                    "MachineId": machine_id,
                    "SensorId": sensor_id,
                    "Value": value
                }
                
                batch_data.append(data)
                
            # Send the batch data to RabbitMQ and log it to XML
            self.send_to_rabbitmq(json.dumps(batch_data))
            self.log_data_to_xml(batch_data)
            
            # Sleep for a different duration depending on the current hour
            current_hour = datetime.now().hour
            if 9 <= current_hour <= 17:
                time.sleep(180)  
            else:
                time.sleep(300)  

    @staticmethod
    def is_connected():
        """
        Check if there is an internet connection.
        
        :return: bool, whether there is an internet connection or not
        """
        try:
            # Try to create a socket connection to Google's main server
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            pass
        return False


# Sensor data
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
# Create a SensorSimulator instance and start the simulation
simulator = SensorSimulator(sensor_data)
simulator.simulate()
