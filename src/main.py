import json


def display_route(route):
    print("\nYour journey:")

    for number, station in enumerate(route, start=1):
        print(f"{number}. {station}")

    print(f"\nStops travelled: {len(route) - 1}")


def calculate_route(stations, start_station, destination):

    start_index = stations.index(start_station)
    destination_index = stations.index(destination)

    if start_index < destination_index:
        route = stations[start_index : destination_index + 1]

    elif start_index > destination_index:
        route = stations[destination_index : start_index + 1]
        route.reverse()

    else:
        route = [start_station]

    return route


def find_station_lines(underground, station_name):
    lines = []

    for line_name, stations in underground.items():
        if station_name in stations:
            lines.append(line_name)

    return lines


def find_best_interchange(
    underground, start_station, destination, interchanges, start_line, destination_line
):

    best_route = None
    best_interchange = None

    for interchange in interchanges:

        first_route = calculate_route(
            underground[start_line], start_station, interchange
        )

        second_route = calculate_route(
            underground[destination_line], interchange, destination
        )

        complete_route = first_route + second_route[1:]

        if best_route is None or len(complete_route) < len(best_route):
            best_route = complete_route
            best_interchange = interchange

    return best_route, best_interchange

def find_common_lines(start_lines, destination_lines):

    common_lines = []

    for line in start_lines:
        if line in destination_lines:
            common_lines.append(line)

    return common_lines

def find_interchanges(underground, first_line, second_line):
    interchanges = []

    for station in underground[first_line]:
        if station in underground[second_line]:
            interchanges.append(station)

    return interchanges

with open("data/stations.json", "r") as file:
    underground = json.load(file)
# Find stations shared by the Victoria and Piccadilly lines

interchanges = find_interchanges(underground, "Victoria", "Piccadilly")

start_station = input("Enter Your Starting Station: ")
destination = input("Enter Your Destination: ")

start_lines = find_station_lines(underground, start_station)
destination_lines = find_station_lines(underground, destination)

common_lines = find_common_lines(start_lines, destination_lines)

if not common_lines:
    print("Different lines detected")
    print("Possible starting lines:", start_lines)
    print("Possible destination lines:", destination_lines)

if common_lines:

    line = common_lines[0]

    route = calculate_route(underground[line], start_station, destination)

    display_route(route)

elif "Victoria" in start_lines and "Piccadilly" in destination_lines:

    route, interchange = find_best_interchange(
        underground, start_station, destination, interchanges, "Victoria", "Piccadilly"
    )

    print(f"\nChange trains at: {interchange}")
    display_route(route)

elif "Piccadilly" in start_lines and "Victoria" in destination_lines:
    route, interchange = find_best_interchange(
        underground, destination, start_station, interchanges, "Victoria", "Piccadilly"
    )

    route.reverse()
    print(f"\nChange trains at: {interchange}")
    display_route(route)

else:
    print("This journey is not supported yet.")
