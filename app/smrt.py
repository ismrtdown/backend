import app

AL = {}
OFFICIALLY_DELAYED_THRESHOLD = 10
MARGIN = 3

class Node:
    # station_code: Station ID of the station i.e., DT29
    # station_name: Station Name of the station
    def __init__(self, station_code, station_name):
        self.station_code = station_code
        self.station_name = station_name

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

        if station_info[number] > 1:
            prev_station_code = 

        # WARNING: PLACEHOLDER
        prev_node = Node(station_code, station_name)
        next_node = Node(station_code, station_name)

        AL[station_code] = [prev_node, next_node] 

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
