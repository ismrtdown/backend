import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response
from supabase import create_client, Client
from postgrest.exceptions import APIError

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
THRESHOLD = 10

app = Flask("sad")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



mrt_station_codes = [
    "NS1","NS2","NS3","NS4","NS5","NS7","NS8","NS9","NS10","NS11","NS12",
    "NS13","NS14","NS15","NS16","NS17","NS18","NS19","NS20","NS21","NS22",
    "NS23","NS24","NS25","NS26","NS27","NS28",

    "EW1","EW2","EW3","EW4","EW5","EW6","EW7","EW8","EW9","EW10","EW11",
    "EW12","EW13","EW14","EW15","EW16","EW17","EW18","EW19","EW20","EW21",
    "EW22","EW23","EW24","EW25","EW26","EW27","EW28","EW29","EW30","EW31",
    "EW32","EW33",

    "CG1","CG2",

    "NE1","NE3","NE4","NE5","NE6","NE7","NE8","NE9","NE10","NE11","NE12",
    "NE13","NE14","NE15","NE16","NE17","NE18",

    "CC1","CC2","CC3","CC4","CC5","CC6","CC7","CC8","CC9","CC10","CC11",
    "CC12","CC13","CC14","CC15","CC16","CC17","CC19","CC20","CC21","CC22",
    "CC23","CC24","CC25","CC26","CC27","CC28","CC29",

    "CE1","CE2",

    "DT1","DT2","DT3","DT4","DT5","DT6","DT7","DT8","DT9","DT10","DT11",
    "DT12","DT13","DT14","DT15","DT16","DT17","DT18","DT19","DT20","DT21",
    "DT22","DT23","DT24","DT25","DT26","DT27","DT28","DT29","DT30","DT31",
    "DT32","DT33","DT34","DT35",

    "BP1","BP2","BP3","BP4","BP5","BP6","BP7","BP8","BP9","BP10","BP11",
    "BP12","BP13",

    "STC",

    "SE1","SE2","SE3","SE4","SE5",
    "SW1","SW2","SW3","SW4","SW5","SW6","SW7","SW8",

    "PTC",

    "PE1","PE2","PE3","PE4","PE5","PE6","PE7",
    "PW1","PW2","PW3","PW4","PW5","PW6","PW7",

    "TE1","TE2","TE3","TE4","TE5","TE6","TE7","TE8","TE9","TE11","TE12",
    "TE13","TE14","TE15","TE16","TE17","TE18","TE19","TE20","TE22","TE23",
    "TE24","TE25","TE26","TE27","TE28","TE29"
]

def report_post(data):
    if not "station_code" in data:
        error = {
            "error": "station code missing!"
        }
        return error, 400
    station_code = data["station_code"]
    line = station_code[:2]
    station_number = station_code[2: ]
    if not station_code in mrt_station_codes:
        error = {
            "error": "invalid station!"
        }
        return error, 400
    try:
        row_data = {
            "station_code": station_code,
            "created_by": request.remote_addr
        }
        supabase.table("down_reports").insert([row_data]).execute()
        success = {
            "error": "success!"
        }
        return success, 200
    except APIError as e:
        error = {
            "error": "server error"
        }
        print(e)
        return error, 500

def report_get():
    try:
        time_now = datetime.now(tz= timezone.utc)
        start = time_now - timedelta(minutes=30)
        response = supabase.table("down_reports").select("station_code", "created_at").gte("created_at",start.isoformat()).execute()
        reports = response.data
        no_of_reports = {}
        for x in  mrt_station_codes:
            no_of_reports[x] = [0, 0]
        for report in reports:
            if (time_now - datetime.fromisoformat(report["created_at"])).total_seconds() / 60 <= 5:
                # red
                no_of_reports[report["station_code"]][0] += 1
            else:
                # yellow
                no_of_reports[report["station_code"]][1] += 1
        res = {}
        for station in no_of_reports.keys():
            print(station)
            station_reports = no_of_reports[station]
            if station_reports[0] > THRESHOLD:
                res[station] = 2
            elif station_reports[0] + station_reports[1] > THRESHOLD:
                res[station] = 1
            else:
                res[station] = 0
        return res, 200
    except APIError as e:
        error = {
            "error": "server error"
        }
        print(e)
        return error, 500

@app.route("/report", methods = ["GET", "POST"])
def report():
    print(request.method)
    if request.method == "POST":
        return report_post(request.get_json())
    else:
        return report_get()

@app.get("/")
def root():
    return {"ping": "pong"}
