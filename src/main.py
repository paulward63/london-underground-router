import json

from display import (
    display_route,
    display_journey_lines,
    display_dijkstra_journey
)
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

result = find_fewest_interchanges_route(
    underground, network, start_station, destination
)

if result is not None:
    fewest_changes_route, route_lines = result

    print("\nFewest-interchanges route:")
    print(fewest_changes_route)
    print("Lines used:", " → ".join(dict.fromkeys(route_lines)))

    print("Stops:", len(fewest_changes_route) - 1)
    print(
        "Interchanges:",
        sum(route_lines[i] != route_lines[i - 1] for i in range(1, len(route_lines))),
    )
    
    display_dijkstra_journey(fewest_changes_route, route_lines)

else:
    print("No route found.")

if start_station not in network:
    print(f"Unknown starting station: {start_station}")

elif destination not in network:
    print(f"Unknown destination: {destination}")

else:
    route = find_shortest_route(network, start_station, destination)

    print("DEBUG: Starting alternative route search...", flush=True)

    # all_routes = find_all_shortest_routes(
    #    network, start_station, destination
    # )

    all_routes = [fewest_changes_route]

    print("DEBUG: Alternative route search finished!", flush=True)

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

    def display_dijkstra_journey(route, route_lines):
        print("\nYour journey instructions:")

        if not route:
            print("No journey available.")
            return

        if not route_lines:
            print("You are already at your destination.")
            return

        print(f"Board the {route_lines[0]} Line at {route[0]}.")

        for i in range(1, len(route_lines)):
            if route_lines[i] != route_lines[i - 1]:
                print(f"Change to the {route_lines[i]} Line at {route[i]}.")

        print(f"Alight at {route[-1]}.")
