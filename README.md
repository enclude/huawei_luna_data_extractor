# Łącznik do wyodrębniania danych z falownika Huawei SUN2000-KTL z możliwością publikacji w PSQL (PostgreSQL) oraz MQTT

Możliwość monitorowania inwertera Huawei SUN2000-KTL trójfazowego. Możliwość przesyłania danych do wskazanego brokera MQTT, bazy danych PSQL oraz wystawia plik JSON z odczytanymi wartościami. 

## Wymagania:
1. Docker
2. Opcjonalnie: PSQL
3. Opcjonalnie: Broker MQTT

## Aby uruchomić
Sklonuj to repozytorium oraz zbuduj obraz dockera za pomocą komendy:
`docker build -t huawei-solar .`

Po prawidłowym zbudowaniu obrazu możesz użyć w ramach docker-compose. MQTT i PSQL przyjmują wartości "True" albo "False". True dla korzystania z tej opcji, False dla wyłączenia. 
```
huawei-solar:
    container_name: huawei-solar
    restart: unless-stopped
    image: huawei-solar:latest
    ports:
      - "8000:8000"
    environment:
      - INVERTER_IP=XXX.XXX.XXX.XXX
      - MQTT_HOST=XXX.XXX.XXX.XXX
      - DB_SERVER=XXX.XXX.XXX.XXX
      - DB_NAME=XXX.XXX.XXX.XXX
      - DB_USER=XXX.XXX.XXX.XXX
      - DB_PASS=XXX.XXX.XXX.XXX
      - DB_TABLE=inverter
      - MQTT=True
      - PSQL=True
```
 
 ## Współpraca z MQTT
![Zrzut ekranu z MQTT Explorera](https://raw.githubusercontent.com/enclude/huawei_luna_data_extractor/main/images/mqtt.png)
 
 ## Prezentacja danych po JSON
 Po uruchomieniu kontenera dostęny będzie plik: `http://<DOCKER_IP>:8002/huawei.json` z wartościami. Opis wartości znajduje się w pliku "raw/huawei_opis.txt"
 
 ## Współpraca z PSQL
 Tworzenie tabeli (musi być zgodna ze zmienną DB_TABLE; zamienić wartość `public.converter` na `public.DB_TABLE`):
 ```CREATE TABLE public.inverter (
    "timestamp" timestamp with time zone DEFAULT clock_timestamp() NOT NULL,
    id bigint NOT NULL,
    pv_01_voltage numeric NOT NULL,
    pv_01_current numeric NOT NULL,
    pv_02_voltage numeric NOT NULL,
    pv_02_current numeric NOT NULL,
    line_voltage_a_b numeric NOT NULL,
    line_voltage_b_c numeric NOT NULL,
    line_voltage_c_a numeric NOT NULL,
    phase_a_voltage numeric NOT NULL,
    phase_b_voltage numeric NOT NULL,
    phase_c_voltage numeric NOT NULL,
    phase_a_current numeric NOT NULL,
    phase_b_current numeric NOT NULL,
    phase_c_current numeric NOT NULL,
    day_active_power_peak integer NOT NULL,
    active_power integer NOT NULL,
    reactive_power integer NOT NULL,
    power_factor numeric NOT NULL,
    grid_frequency numeric NOT NULL,
    efficiency numeric NOT NULL,
    internal_temperature numeric NOT NULL,
    insulation_resistance numeric NOT NULL,
    device_status character varying NOT NULL,
    fault_code numeric NOT NULL,
    startup_time character varying NOT NULL,
    shutdown_time character varying NOT NULL,
    meter_status character varying NOT NULL,
    grid_a_voltage numeric NOT NULL,
    grid_b_voltage numeric NOT NULL,
    grid_c_voltage numeric NOT NULL,
    active_grid_a_current numeric NOT NULL,
    active_grid_b_current numeric NOT NULL,
    active_grid_c_current numeric NOT NULL,
    power_meter_active_power integer NOT NULL,
    active_grid_power_factor numeric NOT NULL,
    active_grid_frequency numeric NOT NULL,
    grid_exported_energy numeric NOT NULL,
    grid_accumulated_energy numeric NOT NULL,
    meter_type character varying NOT NULL,
    active_grid_a_b_voltage numeric NOT NULL,
    active_grid_b_c_voltage numeric NOT NULL,
    active_grid_c_a_voltage numeric NOT NULL,
    active_grid_a_power integer NOT NULL,
    active_grid_b_power integer NOT NULL,
    active_grid_c_power integer NOT NULL,
    storage_state_of_capacity numeric NOT NULL,
    storage_running_status character varying(7) NOT NULL,
    storage_bus_voltage numeric NOT NULL,
    storage_bus_current numeric NOT NULL,
    storage_charge_discharge_power numeric NOT NULL,
    storage_total_charge numeric NOT NULL,
    storage_total_discharge numeric NOT NULL,
    storage_current_day_charge_capacity numeric NOT NULL,
    storage_current_day_discharge_capacity numeric NOT NULL,
    p_max integer NOT NULL,
    s_max integer NOT NULL,
    q_max_out integer NOT NULL,
    q_max_in integer NOT NULL,
    daily_yield_energy numeric NOT NULL,
    storage_unit_1_battery_pack_1_voltage numeric NOT NULL,
    storage_unit_1_battery_pack_1_current numeric NOT NULL,
    storage_unit_1_battery_pack_1_state_of_capacity numeric NOT NULL,
    storage_unit_1_battery_pack_2_voltage numeric NOT NULL,
    storage_unit_1_battery_pack_2_current numeric NOT NULL,
    storage_unit_1_battery_pack_2_state_of_capacity numeric NOT NULL,
    storage_unit_1_battery_temperature numeric NOT NULL
);
```

## Współpraca z Supla Device
Plik JSON można użyć w https://github.com/SUPLA/supla-device jako kanał "ElectricityMeterParsed". 
Przykład konfiguracyjny dla tego kanału gdy podłączony jest liczni energii elektrycznej
```
  - type: ElectricityMeterParsed
    parser:
      type: Json
    source:
      type: File
      file: huawei.json
    frequency: grid_frequency
    phase_1:
      - voltage: grid_A_voltage
      - current: active_grid_A_current
      - power_active: active_grid_A_power
    phase_3:
      - voltage: grid_C_voltage
      - current: active_grid_C_current
      - power_active: active_grid_C_power
      - fwd_act_energy: grid_accumulated_energy
      - rvr_act_energy: grid_exported_energy
    phase_2:
      - voltage: grid_B_voltage
      - current: active_grid_B_current
      - power_active: active_grid_B_power

```

### Bazowane na:
https://github.com/ccorderor/huawei-sun2000-modbus-mqtt

https://gitlab.com/Emilv2/huawei-solar
