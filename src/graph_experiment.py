import json
from graph import build_graph

network = {
    "Brixton": ["Stockwell"],
    "Stockwell": ["Brixton", "Vauxhall"],
    "Vauxhall": ["Stockwell", "Pimlico"],
    "Pimlico": ["Vauxhall"],
}


def find_connection_lines(underground, station_a, station_b):
    connecting_lines = []

    for line_name, stations in underground.items():

        if isinstance(stations, dict):
            station_lists = stations.values()
        else:
            station_lists = [stations]

        for station_list in station_lists:
            for i in range(len(station_list) - 1):

                if (
                    station_list[i] == station_a and station_list[i + 1] == station_b
                ) or (
                    station_list[i] == station_b and station_list[i + 1] == station_a
                ):
                    if line_name not in connecting_lines:
                        connecting_lines.append(line_name)

    return connecting_lines


def count_interchanges(underground, route):
    previous_line = None
    interchange_count = 0

    for i in range(len(route) - 1):
        station_a = route[i]
        station_b = route[i + 1]

        lines = find_connection_lines(underground, station_a, station_b)

        current_line = lines[0]

        if previous_line is not None and current_line != previous_line:
            interchange_count += 1

        previous_line = current_line

    return interchange_count

def find_shortest_route(network, start_station, destination):
    queue = [[start_station]]
    visited = [start_station]

    while queue:
        route = queue.pop(0)
        current_station = route[-1]

        if current_station == destination:
            return route

        for connected_station in network[current_station]:
            if connected_station not in visited:
                visited.append(connected_station)

                new_route = route + [connected_station]
                queue.append(new_route)

    return None


def find_all_shortest_routes(network, start_station, destination):
    queue = [[start_station]]
    shortest_routes = []
    shortest_length = None

    while queue:
        route = queue.pop(0)

        if shortest_length is not None and len(route) > shortest_length:
            break

        current_station = route[-1]

        if current_station == destination:
            shortest_routes.append(route)
            shortest_length = len(route)
            continue

        for connected_station in network[current_station]:
            if connected_station not in route:
                new_route = route + [connected_station]
                queue.append(new_route)

    return shortest_routes


with open("data/stations.json", "r") as file:
    underground = json.load(file)

network = build_graph(underground)

start_station = input("Enter starting station: ").strip()
destination = input("Enter destination station: ").strip()

if start_station not in network:
    print(f"Unknown starting station: {start_station}")

elif destination not in network:
    print(f"Unknown destination: {destination}")

else:
    route = find_shortest_route(network, start_station, destination)

    if route:
        print(f"\nRoute found: {' -> '.join(route)}")
        print(f"Number of stops: {len(route) - 1}")
    else:
        print("No route found.")

print("\nTesting station connections:")

print(find_connection_lines(underground, "Finsbury Park", "Arsenal"))

print(find_connection_lines(underground, "Finsbury Park", "Highbury & Islington"))


print(find_connection_lines(underground, "Finsbury Park", "Arsenal"))

print(find_connection_lines(underground, "Finsbury Park", "Highbury & Islington"))

print(find_connection_lines(underground, "Hatton Cross", "Heathrow Terminal 5"))

print("\nChecking for line changes:")

if start_station in network and destination in network and route:
    previous_line = None
    interchange_count = 0

    for i in range(len(route) - 1):
        station_a = route[i]
        station_b = route[i + 1]

        lines = find_connection_lines(underground, station_a, station_b)

        current_line = lines[0]

        if previous_line is not None and current_line != previous_line:
            interchange_count += 1
            print(f"Change from {previous_line} to {current_line} at {station_a}")

        previous_line = current_line

    print(f"\nTotal interchanges: {interchange_count}")

routes = find_all_shortest_routes(network, "Finsbury Park", "Caledonian Road")

print("\nAll shortest routes:")

for route_option in routes:
    print(" -> ".join(route_option))

    changes = count_interchanges(underground, route_option)

    print(f"Stops: {len(route_option) - 1}")
    print(f"Interchanges: {changes}")
    print()


best_route = min(
    routes, key=lambda route_option: count_interchanges(underground, route_option)
)

print("\nRecommended journey:")
print(" -> ".join(best_route))
