import json

from display import display_route, display_journey_lines
from routing import (
    find_shortest_route,
    find_all_shortest_routes,
    count_interchanges,
    find_fewest_interchanges_route,
)
from graph import build_graph

with open("data/stations.json", "r") as file:
    underground = json.load(file)

network = build_graph(underground)

# print("Camden Town neighbours:", network["Camden Town"])

print(f"Network successfully built with {len(network)} stations.")


start_station = input("Enter Your Starting Station: ").strip()
destination = input("Enter Your Destination: ").strip()

fewest_changes_route = find_fewest_interchanges_route(
    underground, network, start_station, destination
)

print("\nFewest-interchanges route:")
print(fewest_changes_route)

if fewest_changes_route is not None:
    print("Stops:", len(fewest_changes_route) - 1)
    print("Interchanges:", count_interchanges(underground, fewest_changes_route))

if start_station not in network:
    print(f"Unknown starting station: {start_station}")

elif destination not in network:
    print(f"Unknown destination: {destination}")

else:
    route = find_shortest_route(network, start_station, destination)

    all_routes = find_all_shortest_routes(
        network, start_station, destination
    )

    print("\nAlternative shortest routes:")    

    for route_option in all_routes:
        print(" -> ".join(route_option))
        changes = count_interchanges(underground, route_option)
        print(f"Interchanges: {changes}")

    best_route = min(
        all_routes,
        key=lambda route_option: count_interchanges(underground, route_option),
    )

    print("\nRecommended journey:")
    display_route(best_route)
    display_journey_lines(underground, best_route)

    best_changes = count_interchanges(underground, best_route)
    print(f"Interchanges required: {best_changes}")
