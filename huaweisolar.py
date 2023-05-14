import time
from huawei_solar import *
import huawei_solar
import paho.mqtt.client
import os
import json
import psycopg2

import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


inverter_ip = os.getenv('INVERTER_IP')
mqtt_host = os.getenv('MQTT_HOST')

db_server = os.getenv('DB_SERVER')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')

# SQL
# Definiowanie połączenia SQL
sql_connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_server)

inverter = huawei_solar.HuaweiSolar(inverter_ip, port=502, slave=1)
inverter._slave = 1
inverter.wait = 1

def modbusAccess():

    vars = ['pv_01_voltage', 'pv_01_current', 'pv_02_voltage', 'pv_02_current', 'line_voltage_A_B', 'line_voltage_B_C', 'line_voltage_C_A', 'phase_A_voltage', 'phase_B_voltage', 'phase_C_voltage', 'phase_A_current', 'phase_B_current', 'phase_C_current', 'day_active_power_peak', 'active_power', 'reactive_power', 'power_factor', 'grid_frequency', 'efficiency', 'internal_temperature', 'insulation_resistance', 'device_status', 'fault_code', 'startup_time', 'shutdown_time', 'meter_status', 'grid_A_voltage', 'grid_B_voltage', 'grid_C_voltage', 'active_grid_A_current', 'active_grid_B_current', 'active_grid_C_current', 'power_meter_active_power', 'power_meter_reactive_power', 'active_grid_power_factor', 'active_grid_frequency', 'grid_exported_energy', 'grid_accumulated_energy', 'meter_type', 'active_grid_A_B_voltage', 'active_grid_B_C_voltage', 'active_grid_C_A_voltage', 'active_grid_A_power', 'active_grid_B_power', 'active_grid_C_power', 'storage_state_of_capacity', 'storage_running_status', 'storage_bus_voltage', 'storage_bus_current', 'storage_charge_discharge_power', 'storage_total_charge', 'storage_total_discharge', 'storage_current_day_charge_capacity', 'storage_current_day_discharge_capacity', 'day_active_power_peak', 'P_max', 'S_max', 'Q_max_out', 'Q_max_in', 'daily_yield_energy', 'storage_unit_1_battery_pack_1_voltage', 'storage_unit_1_battery_pack_1_current', 'storage_unit_1_battery_pack_1_state_of_capacity', 'storage_unit_1_battery_pack_2_voltage', 'storage_unit_1_battery_pack_2_current', 'storage_unit_1_battery_pack_2_state_of_capacity', 'storage_unit_1_battery_temperature']
    reads = {}

    while True:

        for i in vars:
            try:
                mid = inverter.get(i)

                clientMQTT.publish(topic="emon/NodeHuawei/"+i, payload= str(mid.value), qos=1, retain=False)
                reads[i] = str(mid.value)

            except:
                pass

        with open("huawei.json", "w") as outfile:
            json.dump(reads, outfile)

        sql = "INSERT INTO TA2260010724 ("
        cur = sql_connection.cursor()

        j = 0
        for i in reads:
            if j == 0:
                sql = sql + i
                j = j + 1
            else:
                sql = sql + ", " + i

        sql = sql + ") VALUES ("

        j = 0
        for i in reads:
            if j == 0:
                sql = sql + "'" + reads[i] +"'"
                j = j + 1
            else:
                sql = sql + ", '" + reads[i] +"'"
        sql = sql + ");"
        print(sql)

        cur.execute(sql)
        sql_connection.commit()

        time.sleep(0.15)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        log.info("MQTT OK!")
    else:
        log.info("MQTT FAILURE. ERROR CODE: %s",rc)

paho.mqtt.client.Client.connected_flag=False #create flag in class
broker_port = 1883

clientMQTT = paho.mqtt.client.Client()
clientMQTT.on_connect=on_connect #bind call back function
clientMQTT.loop_start()
log.info("Connecting to MQTT broker: %s ",mqtt_host)
clientMQTT.username_pw_set(username="",password="")
clientMQTT.connect(mqtt_host, broker_port) #connect to broker
while not clientMQTT.connected_flag: #wait in loop
    log.info("...")
time.sleep(0.5)
log.info("START MODBUS...")

modbusAccess()

clientMQTT.loop_stop()