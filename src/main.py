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
        route = stations[start_index:destination_index + 1]

    elif start_index > destination_index:
        route = stations[destination_index:start_index + 1]
        route.reverse()

    else:
        route = [start_station]

    return route

with open("data/stations.json", "r") as file:
    underground = json.load(file)

# for station in underground["Victoria"]:
#   print(station)

start_station = input("Enter Your Starting Station: ")
destination = input("Enter Your Destination: ")

if start_station in underground["Victoria"] and destination in underground["Victoria"]:

    route = calculate_route(
        underground["Victoria"],
        start_station,
        destination
    )

    display_route(route)

else:
    print("One or both stations are not on the Victoria Line.")
