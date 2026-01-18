import os
import math
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from flask import Flask, request
from supabase import create_client, Client
from postgrest.exceptions import APIError
from helper import get_mrt_lines
from smrt import get_range_of_breakdowns 
from flask_cors import CORS

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
THRESHOLD = 10

stations = get_mrt_lines()
mrt_station_codes = stations.keys()

app = Flask("sad")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
cache = []
prev_record = datetime.now(tz=timezone.utc) - timedelta(days=1)
CORS(app, resources={r"*": {"origins": ["http://localhost:3000", "https://ismrtdown.github.io"]}})


async def get_graph_data():
    try:
        res = [] 
        now = datetime.now(tz=timezone.utc)
        yest = now - timedelta(days=1)
        for i in range(96):
            data = {
                "time": yest + timedelta(minutes=15) * i,
                "no": 0
            }
            res.append(data)
        response = supabase.table("down_reports").select("station_code", "created_at").gte("created_at",yest.isoformat()).lte("created_at", now.isoformat()).execute()
        for report in response.data:
            index = math.floor((datetime.fromisoformat(report["created_at"]) - yest).total_seconds() / 60 / 15)
            res[index]["no"] += 1
        return res
    except APIError:
        return None
    
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
            if (time_now - datetime.fromisoformat(report["created_at"])).total_seconds() / 60 <= 10:
                # red
                no_of_reports[report["station_code"]][0] += 1
            else:
                # yellow
                no_of_reports[report["station_code"]][1] += 1
        res = {}
        for station in no_of_reports.keys():
            #print(station)
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

@app.route("/reportno", methods = ["GET"])
async def reportno():
    global cache, prev_record
    now = datetime.now(tz = timezone.utc)
    if (now - prev_record).total_seconds() / 60 > 1:
        cache = await get_graph_data()
        if cache is None:
            error = {
                "error": "server error"
            }
            return error, 500
        prev_record = now
    return cache, 200
        
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

@app.get("/range-delayed")
def range_delayed():
    report_data = report_get()
    return get_range_of_breakdowns(stations, report_data)

