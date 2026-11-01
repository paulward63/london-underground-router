import json

network = {
    "Brixton": ["Stockwell"],
    "Stockwell": ["Brixton", "Vauxhall"],
    "Vauxhall": ["Stockwell", "Pimlico"],
    "Pimlico": ["Vauxhall"],
}


def build_graph(underground):
    graph = {}

    for line_name, stations in underground.items():
        for i in range(len(stations) - 1):
            station_a = stations[i]
            station_b = stations[i + 1]

            if station_a not in graph:
                graph[station_a] = []

            if station_b not in graph:
                graph[station_b] = []

            if station_b not in graph[station_a]:
                graph[station_a].append(station_b)

            if station_a not in graph[station_b]:
                graph[station_b].append(station_a)

    return graph


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

