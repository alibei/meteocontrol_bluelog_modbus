from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
import os
import RPi.GPIO as GPIO

# Variables
RELAIS_1_GPIO = 16    # Relay 1
RELAIS_2_GPIO = 18    # Relay 2
RELAIS_3_GPIO = 22    # Relay 3
MODBUS_CLIENT = ModbusClient('192.168.2.45', port=502)

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
GPIO.setup(RELAIS_2_GPIO, GPIO.OUT)
GPIO.setup(RELAIS_3_GPIO, GPIO.OUT)

GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
GPIO.output(RELAIS_2_GPIO, GPIO.HIGH)
GPIO.output(RELAIS_3_GPIO, GPIO.HIGH)

# Connect Modbus client
MODBUS_CLIENT.connect()

# Disconnect Modbus client
def on_disconnect(client, userdata, rc):
        global MODBUS_CLIENT

        logging.info("Connection lost, end modbus client")

        MODBUS_CLIENT.close()

# Handle payload
def get_data_payload():
        """Get some data payload"""
        global MODBUS_CLIENT

        # Recieve and decode remote power
        readPPC_P_SET_REL = MODBUS_CLIENT.read_holding_registers(104, 1, unit=10)  #Remote Power Control License
        registersPPC_P_SET_REL = readPPC_P_SET_REL.registers

        # Print remote power percentage
        print(registersPPC_P_SET_REL)

        # Switch the relays
        if (registersPPC_P_SET_REL[0] < 30):              # If remote power is < 30%
                 GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
                 GPIO.output(RELAIS_2_GPIO, GPIO.LOW)
                 GPIO.output(RELAIS_3_GPIO, GPIO.LOW)
        else:                                               # If remote power is >= 30%
                 GPIO.output(RELAIS_3_GPIO, GPIO.HIGH)
                 GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
                 GPIO.output(RELAIS_2_GPIO, GPIO.HIGH)

while(True):
        get_data_payload()
        time.sleep(5)
