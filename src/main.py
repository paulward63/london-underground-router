import json

from display import display_route
from routing import find_shortest_route
from graph import build_graph

with open("data/stations.json", "r") as file:
    underground = json.load(file)

network = build_graph(underground)

print(f"Network successfully built with {len(network)} stations.")


start_station = input("Enter Your Starting Station: ").strip()
destination = input("Enter Your Destination: ").strip()

if start_station not in network:
    print(f"Unknown starting station: {start_station}")

elif destination not in network:
    print(f"Unknown destination: {destination}")

else:
    route = find_shortest_route(network, start_station, destination)

    if route:
        display_route(route)
    else:
        print("No route found.")
