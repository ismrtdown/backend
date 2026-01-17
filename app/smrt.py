import json

AL = {}
OFFICIALLY_DELAYED_THRESHOLD = 10
MARGIN = 3

FAKE_REPORT_DATA = {"BP1":0,"BP10":0,"BP11":0,"BP12":0,"BP13":0,"BP14":0,"BP2":0,"BP3":0,"BP4":0,"BP5":0,"BP6":0,"BP7":0,"BP8":0,"BP9":0,"CC1":0,"CC10":0,"CC11":0,"CC12":0,"CC13":0,"CC14":0,"CC15":0,"CC16":0,"CC17":0,"CC18":0,"CC19":0,"CC2":0,"CC20":0,"CC21":0,"CC22":0,"CC23":0,"CC24":0,"CC25":0,"CC26":0,"CC27":0,"CC28":0,"CC29":0,"CC3":0,"CC30":0,"CC31":0,"CC32":0,"CC4":0,"CC5":0,"CC6":0,"CC7":0,"CC8":0,"CC9":0,"CE1":0,"CE2":0,"CG":0,"CG1":0,"CG2":0,"CP1":0,"CP2":0,"CP3":0,"CP4":0,"CR1":0,"CR10":0,"CR11":0,"CR12":0,"CR13":0,"CR14":0,"CR15":0,"CR16":0,"CR17":0,"CR18":0,"CR19":0,"CR2":0,"CR21":0,"CR3":0,"CR4":0,"CR5":0,"CR6":0,"CR7":0,"CR8":0,"CR9":0,"DE1":0,"DE2":0,"DT1":0,"DT10":0,"DT11":0,"DT12":0,"DT13":0,"DT14":0,"DT15":0,"DT16":0,"DT17":0,"DT18":0,"DT19":0,"DT2":0,"DT20":0,"DT21":0,"DT22":0,"DT23":0,"DT24":0,"DT25":0,"DT26":0,"DT27":0,"DT28":0,"DT29":0,"DT3":0,"DT30":0,"DT31":0,"DT32":0,"DT33":0,"DT34":0,"DT35":0,"DT36":0,"DT37":0,"DT4":0,"DT5":0,"DT6":0,"DT7":0,"DT8":0,"DT9":0,"EW1":0,"EW10":0,"EW11":0,"EW12":0,"EW13":0,"EW14":0,"EW15":0,"EW16":0,"EW17":0,"EW18":0,"EW19":0,"EW2":0,"EW20":0,"EW21":0,"EW22":0,"EW23":0,"EW24":0,"EW25":0,"EW26":0,"EW27":0,"EW28":0,"EW29":0,"EW3":0,"EW30":0,"EW31":0,"EW32":0,"EW33":0,"EW4":0,"EW5":0,"EW6":0,"EW7":0,"EW8":0,"EW9":0,"JE1":0,"JE2":0,"JE3":0,"JE4":0,"JE5":0,"JE6":0,"JE7":0,"JS1":0,"JS10":0,"JS11":0,"JS12":0,"JS2":0,"JS3":0,"JS4":0,"JS5":0,"JS6":0,"JS7":0,"JS8":0,"JS9":0,"JW1":0,"JW2":0,"JW3":0,"JW4":0,"JW5":0,"NE1":0,"NE10":0,"NE11":0,"NE12":0,"NE13":0,"NE14":0,"NE15":0,"NE16":0,"NE17":0,"NE18":0,"NE3":0,"NE4":0,"NE5":0,"NE6":0,"NE7":0,"NE8":0,"NE9":0,"NS1":0,"NS10":0,"NS11":0,"NS12":0,"NS13":0,"NS14":0,"NS15":0,"NS16":0,"NS17":0,"NS18":0,"NS19":0,"NS2":0,"NS20":0,"NS21":0,"NS22":0,"NS23":0,"NS24":0,"NS25":0,"NS26":0,"NS27":0,"NS28":0,"NS3":0,"NS3A":0,"NS4":0,"NS5":0,"NS6":0,"NS7":0,"NS8":0,"NS9":0,"PE1":10,"PE2":0,"PE3":0,"PE4":0,"PE5":0,"PE6":0,"PE7":0,"PTC":10,"PW1":0,"PW2":10,"PW3":0,"PW4":0,"PW5":0,"PW6":10,"PW7":10,"SE1":10,"SE2":0,"SE3":0,"SE4":0,"SE5":0,"STC":10,"SW1":10,"SW2":0,"SW3":0,"SW4":0,"SW5":0,"SW6":0,"SW7":0,"SW8":0,"TE1":0,"TE10":0,"TE11":0,"TE12":0,"TE13":0,"TE14":0,"TE15":0,"TE16":0,"TE17":0,"TE18":0,"TE19":0,"TE2":0,"TE20":0,"TE21":0,"TE22":0,"TE22A":0,"TE23":0,"TE24":0,"TE25":0,"TE26":0,"TE27":0,"TE28":0,"TE29":10,"TE3":0,"TE30":0,"TE31":10,"TE32":0,"TE33":10,"TE34":10,"TE35":10,"TE4":0,"TE5":0,"TE6":0,"TE7":0,"TE8":0,"TE9":0}

class Node:
    # station_code: Station ID of the station i.e., DT29
    # station_name: Station Name of the station
    def __init__(self, station_code, station_name):
        self.station_code = station_code
        self.station_name = station_name

    def __str__(self):
        return f"Node: {self.station_name} ({self.station_code})"

    def __repr__(self):
        return f"Node: {self.station_name} ({self.station_code})"

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    def __eq__(self, other):
        return self.station_code == other.station_code and self.station_name == other.station_name


def generate_graph(data):
    if AL:
        return AL

    for station_code, station_info in data.items():
        station_name = station_info["name"]
        cur_node = Node(station_code, station_name)

        adjacent_stations = []

        # STC is connected to SE1 and SE5 && SW1 and SW8
        if station_code == "STC":
            adjacent_stations.append(Node("SE1", data["SE1"]["name"]))
            adjacent_stations.append(Node("SE5", data["SE5"]["name"]))
            adjacent_stations.append(Node("SW1", data["SW1"]["name"]))
            adjacent_stations.append(Node("SW8", data["SW8"]["name"]))

        # PTC is connected to PE1 and PE8 && PW1 and PW7
        elif station_code == "PTC":
            adjacent_stations.append(Node("PE1", data["PE1"]["name"]))
            adjacent_stations.append(Node("PE7", data["PE7"]["name"]))
            adjacent_stations.append(Node("PW1", data["PW1"]["name"]))
            adjacent_stations.append(Node("PW7", data["PW7"]["name"]))

        else:
            number = station_info["number"]

            prev_station_code = station_info["line"] + str(number - 1)
            if prev_station_code in data:
                prev_station_name = data[prev_station_code]["name"]
                adjacent_stations.append(Node(prev_station_code, prev_station_name))

            next_station_code = station_info["line"] + str(number + 1)
            if next_station_code in data:
                next_station_name = data[next_station_code]["name"]
                adjacent_stations.append(Node(next_station_code, next_station_name))

            if station_code == "PW1" or station_code == "PW7" or station_code == "PE1" or station_code == "PE7":
                adjacent_stations.append(Node("PTC", data["PTC"]["name"]))

            if station_code == "SW1" or station_code == "SW8" or station_code == "SE1" or station_code == "SE5":
                adjacent_stations.append(Node("STC", data["STC"]["name"]))

        AL[station_code] = adjacent_stations

    return AL


# For each station that is delayed
# Go up and down +-3 stations to check if any other station is also delayed
# Rinse and repeat as needed
# Report the final range
# O(N) where N is the number of stations on that line lol, coz just go to the end of the line worst case (WE GOT VISITED ARRAY)
def check_adjacent_stations(current_station_code, remaining_station_count, furthest_station, data, visited):
    if remaining_station_count == 0:
        return furthest_station

    adjacent_stations = AL[current_station_code]
    for station in adjacent_stations:
        station_code = station.station_code

        if station_code in visited:
            continue

        visited.append(station_code)
        if data[station_code] >= OFFICIALLY_DELAYED_THRESHOLD:
            return check_adjacent_stations(station_code, MARGIN, station, data, visited)
        else:
            return check_adjacent_stations(station_code, remaining_station_count - 1, furthest_station, data, visited)


def get_range_of_breakdowns(station_data, report_data):
    generate_graph(station_data)

    report_data = FAKE_REPORT_DATA

    ranges = []

    for station_code, num_reports in report_data.items():
        if num_reports >= OFFICIALLY_DELAYED_THRESHOLD:
            last_station = check_adjacent_stations(station_code, MARGIN, None, report_data, [station_code])

            if last_station:
                ranges.append([station_code, last_station.station_code])

    # TODO: Merge Intervals

    print(ranges)
    return station_data

