import json
from display import display_route
from stations import find_station_lines, find_common_lines, find_interchanges
from routing import calculate_route, find_best_interchange

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

    for start_line in start_lines:
        for destination_line in destination_lines:
            print("Checking:", start_line, "->", destination_line)

            possible_interchanges = find_interchanges(
                underground, start_line, destination_line
        )

        print("Shared stations:", possible_interchanges)


        if possible_interchanges:
            print("These lines connect!")


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
