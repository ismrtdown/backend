import json

AL = {}
OFFICIALLY_DELAYED_THRESHOLD = 10
MARGIN = 3

class Node:
    # station_code: Station ID of the station i.e., DT29
    # station_name: Station Name of the station
    def __init__(self, station_code, station_name):
        self.station_code = station_code
        self.station_name = station_name

    def __str__(self):
        return f"{self.station_name} ({self.station_code})"

    def __repr__(self):
        return f"{self.station_name} ({self.station_code})"

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

        # STC is connected to SE and SW
        # PTC is connected to PE and PW

        adjacent_stations = []
        number = station_info["number"]

        prev_station_code = station_info["line"] + str(number - 1)
        if prev_station_code in data:
            prev_station_name = data[prev_station_code]["name"]
            adjacent_stations.append(Node(prev_station_code, prev_station_name))

        next_station_code = station_info["line"] + str(number + 1)
        if next_station_code in data:
            next_station_name = data[next_station_code]["name"]
            adjacent_stations.append(Node(next_station_code, next_station_name))

        AL[station_code] = adjacent_stations

    return AL


# For each station that is delayed
# Go up and down +-3 stations to check if any other station is also delayed
# Rinse and repeat as needed
# Report the final range
def check_adjacent_stations(current_station_code, remaining_station_count, furthest_station):
    if remaining_station_count == 0:
        return furthest_station

    # WARNING: Like a bit off? Coz we dont differentiate directions but just work first pls
    adjacent_stations = AL[current_station_code]
    for station in adjacent_stations:
        if data[station] >= OFFICIALLY_DELAYED_THRESHOLD:
            return check_adjacent_stations(station, MARGIN, station)

        else:
            return check_adjacent_stations(station, remaining_station_count - 1, furthest_station)


def get_range_of_breakdowns(station_data, report_data):
    generate_graph(station_data)

    return station_data

    ranges = []

    for station_code, num_reports in report_data.items():
        if num_reports >= OFFICIALLY_DELAYED_THRESHOLD:
            first_station = station_code
            last_station = check_adjacent_stations(first_station, MARGIN, None)

            if last_station:
                ranges.append([first_station, last_station])
