import json

def get_mrt_lines():
    station_names = {}
    with open("mrt_all.json","r") as f:
        data = json.loads(f.read())
        for station in data.keys():
            line_members = data[station]["lineMembers"]
            for lines in line_members.keys():
                for line in line_members[lines]:
                    station_names[line["code"]] =  data[station]["name"]
    return station_names