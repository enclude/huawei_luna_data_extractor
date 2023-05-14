# Łącznik do wyodrębniania danych z falownika Huawei SUN2000-KTL z możliwością publikacji w PSQL (PostgreSQL), JSON oraz MQTT

Możliwość monitorowania inwertera Huawei SUN2000-KTL trójfazowego. Możliwość przesyłania danych do wskazanego brokera MQTT, bazy danych PSQL oraz wystawia plik JSON z odczytanymi wartościami. 

## Wymagania:
1. Docker
2. Opcjonalnie: PSQL (działa na porcie 5432)
3. Opcjonalnie: Broker MQTT (działa na porcie 1883)
4. Włączony MODBUS TCP - https://forum.huawei.com/enterprise/en/modbus-tcp-guide/thread/789585-100027

## Aby uruchomić

### Łatwiejsza droga:
W swoim dockerze zaimportuj obraz: enclude/huawei_luna_data_extractor:latest

### Trochę trudniejsza droga:

Sklonuj to repozytorium oraz zbuduj obraz dockera za pomocą komendy:
`docker build -t huawei-solar .` 

Przed uruchomieniem możesz wyedytować tabelę "vars" w celu dostosowania zmiennych do swojego falownika (usunąć dane dotyczące magazynu, czy dodać dodatkowe stringi).

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
 Tworzenie tabeli (musi być zgodna ze zmienną DB_TABLE; zamienić wartość `public.inverter` na `public.DB_TABLE` lub pozostawić DB_TABLE jako `inverter`):
 ```
 CREATE TABLE public.inverter (
    "timestamp" timestamp with time zone DEFAULT clock_timestamp() NOT NULL,
    id bigint NOT NULL,
    pv_01_voltage numeric,
    pv_01_current numeric,
    pv_02_voltage numeric,
    pv_02_current numeric,
    line_voltage_a_b numeric,
    line_voltage_b_c numeric,
    line_voltage_c_a numeric,
    phase_a_voltage numeric,
    phase_b_voltage numeric,
    phase_c_voltage numeric,
    phase_a_current numeric,
    phase_b_current numeric,
    phase_c_current numeric,
    day_active_power_peak integer,
    active_power integer,
    reactive_power integer,
    power_factor numeric,
    grid_frequency numeric,
    efficiency numeric,
    internal_temperature numeric,
    insulation_resistance numeric,
    device_status character varying,
    fault_code numeric,
    startup_time character varying,
    shutdown_time character varying,
    meter_status character varying,
    grid_a_voltage numeric,
    grid_b_voltage numeric,
    grid_c_voltage numeric,
    active_grid_a_current numeric,
    active_grid_b_current numeric,
    active_grid_c_current numeric,
    power_meter_active_power integer,
    active_grid_power_factor numeric,
    active_grid_frequency numeric,
    grid_exported_energy numeric,
    grid_accumulated_energy numeric,
    meter_type character varying,
    active_grid_a_b_voltage numeric,
    active_grid_b_c_voltage numeric,
    active_grid_c_a_voltage numeric,
    active_grid_a_power integer,
    active_grid_b_power integer,
    active_grid_c_power integer,
    storage_state_of_capacity numeric,
    storage_running_status character varying(7),
    storage_bus_voltage numeric,
    storage_bus_current numeric,
    storage_charge_discharge_power numeric,
    storage_total_charge numeric,
    storage_total_discharge numeric,
    storage_current_day_charge_capacity numeric,
    storage_current_day_discharge_capacity numeric,
    p_max integer,
    s_max integer,
    q_max_out integer,
    q_max_in integer,
    daily_yield_energy numeric,
    storage_unit_1_battery_pack_1_voltage numeric,
    storage_unit_1_battery_pack_1_current numeric,
    storage_unit_1_battery_pack_1_state_of_capacity numeric,
    storage_unit_1_battery_pack_2_voltage numeric,
    storage_unit_1_battery_pack_2_current numeric,
    storage_unit_1_battery_pack_2_state_of_capacity numeric,
    storage_unit_1_battery_temperature numeric);
```

## Współpraca z Supla Device
Plik JSON można użyć w https://github.com/SUPLA/supla-device/blob/main/extras/examples/linux/README.md jako kanał "ElectricityMeterParsed". 
Przykład konfiguracyjny dla tego kanału gdy podłączony jest licznik energii elektrycznej
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
