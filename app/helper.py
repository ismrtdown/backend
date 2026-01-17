import json
import re

def get_mrt_lines():
    lines = {}
    station_names = {}
    with open("mrt_all.json","r") as f:
        data = json.loads(f.read())
        for station in data.keys():
            line_members = data[station]["lineMembers"]
            for lines in line_members.keys():
                for line in line_members[lines]:
                    name = data[station]["name"]
                    mrt_line = lines
                    print(line["code"])
                    number = re.sub(r"[A-Za-z]","0", line["code"][2:])
                    if number == "":
                        number = "0"
                    station_names[line["code"]] =  {
                        "name": data[station]["name"],
                        "line": line["code"][:2],
                        "number": int(number)
                    }
                    station_names
    return station_names

print(get_mrt_lines())