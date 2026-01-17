import os
import random
import math
from dotenv import load_dotenv
from supabase import create_client, Client
from postgrest.exceptions import APIError

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

STATIONS = ['EW18', 'DT13', 'JW5', 'BP9', 'CC30', 'EW15', 'PW7', 'CC13', 'NE12', 'BP7', 'EW11', 'NS22', 'TE14', 'PE2', 'CC17', 'TE9', 'JW3', 'NS14', 'SW7', 'CC31', 'JE4', 'DT22', 'EW27', 'JS8', 'BP4', 'SE5', 'TE5', 'BP10', 'TE18', 'TE3', 'DT33', 'NE1', 'CC29', 'EW6', 'CC6', 'NE4', 'DT19', 'BP12', 'JS6', 'NE18', 'NS5', 'PE7', 'TE19', 'EW31', 'BP13', 'NS13', 'TE23', 'CR6', 'EW21', 'CC22', 'DT37', 'TE31', 'TE6', 'DT28', 'CR16', 'NS18', 'JS11', 'JE7', 'NE9', 'DT5', 'CC14', 'DT8', 'EW8', 'CC9', 'TE16', 'NS19', 'BP3', 'PE4', 'CP3', 'CC10', 'DT26', 'PW2', 'DT31', 'EW26', 'EW14', 'NS26', 'EW12', 'DT14', 'BP14', 'CP2', 'EW28', 'CC5', 'CC7', 'NE15', 'TE8', 'CC23', 'JS5', 'CC18', 'CC11', 'BP2', 'CC27', 'CC32', 'DT7', 'CC24', 'JS9', 'SW8', 'EW32', 'JE2', 'CC28', 'CR10', 'DT3', 'CC4', 'DT15', 'EW23', 'CR17', 'CC16', 'CR7', 'SE4', 'NS11', 'JE3', 'SW3', 'PW4', 'NE16', 'STC', 'TE21', 'PE6', 'PW5', 'CC20', 'JE6', 'NE7', 'DT12', 'TE15', 'CC25', 'CR2', 'BP8', 'TE7', 'CR13', 'DT18', 'NS10', 'SW1', 'JW2', 'NE8', 'PW1', 'CR9', 'CC2', 'TE4', 'DT34', 'DT10', 'TE11', 'EW1', 'CR5', 'CP1', 'CC8', 'TE26', 'PW6', 'TE13', 'BP11', 'DT2', 'SE3', 'NS9', 'TE2', 'EW29', 'NS6', 'DE2', 'NE10', 'JS7', 'NE13', 'CG1', 'DT35', 'TE34', 'CR1', 'TE32', 'EW22', 'NE11', 'CR4', 'EW7', 'NS15', 'NS23', 'CC19', 'DT9', 'NS12', 'CR14', 'EW4', 'CG', 'TE35', 'JW1', 'CC3', 'DT21', 'EW16', 'NE3', 'TE17', 'CG2', 'TE33', 'NS7', 'CR18', 'PE1', 'DT27', 'EW24', 'NS1', 'JE5', 'JS4', 'EW30', 'TE30', 'TE22A', 'SE1', 'SW2', 'DT29', 'SW4', 'EW13', 'NS25', 'JS2', 'JS3', 'TE10', 'BP5', 'CR19', 'PE3', 'DT36', 'NE5', 'SW5', 'NS3', 'TE12', 'CR3', 'TE24', 'NS2', 'DT1', 'BP6', 'DT4', 'NS27', 'TE20', 'CE2', 'EW19', 'PE5', 'TE27', 'TE28', 'TE25', 'EW5', 'NS3A', 'CE1', 'DT16', 'TE29', 'JS12', 'CR21', 'EW2', 'DT32', 'DT17', 'DT30', 'EW10', 'EW3', 'NS21', 'DT11', 'CC26', 'NS20', 'NS8', 'CC21', 'TE1', 'NE14', 'CR8', 'SW6', 'NS17', 'CC15', 'NS4', 'BP1', 'JS1', 'NS16', 'CR11', 'EW20', 'EW17', 'EW33', 'CC12', 'SE2', 'NS24', 'NE6', 'CC1', 'JW4', 'DE1', 'JS10', 'DT25', 'PW3', 'CR12', 'DT20', 'DT23', 'JE1', 'EW25', 'EW9', 'NE17', 'PTC', 'CP4', 'TE22', 'DT6', 'CR15', 'NS28', 'DT24']

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_test_data():
    test_data = {}

    for station_code in STATIONS:
        num_reports = random.randint(0, 20)
        test_data[station_code] = num_reports

    return test_data

def insert_test_data():
    test_data = generate_test_data()

    for station_code, num_reports in test_data.items():
        row_data = {
            "station_code": station_code,
            "created_by": "skull"
        }
        for i in range(num_reports):
            try:
                supabase.table("down_reports_test").insert([row_data]).execute()
            except APIError as e:
                raise Exception(f"SHIT, {e}")

if __name__ == "__main__":
    insert_test_data()
