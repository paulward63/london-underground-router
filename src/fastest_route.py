import heapq
import json

from graph import build_graph
from weighted_graph import (
    load_travel_times,
    build_weighted_graph,
    load_travel_time_corrections,
    apply_travel_time_corrections,
)

def find_fastest_route(weighted_graph, start, destination):
    travel_times = {start: 0}
    previous_stations = {}

    priority_queue = [(0, start)]

    while priority_queue:
        current_time, current_station = heapq.heappop(priority_queue)

        if current_station == destination:
            break

        if current_time > travel_times[current_station]:
            continue

        for neighbour, minutes in weighted_graph[current_station].items():
            new_time = current_time + minutes

            if neighbour not in travel_times or new_time < travel_times[neighbour]:
                travel_times[neighbour] = new_time
                previous_stations[neighbour] = current_station

                heapq.heappush(priority_queue, (new_time, neighbour))

    if destination not in travel_times:
        return None

    route = []
    station = destination

    while station != start:
        route.append(station)
        station = previous_stations[station]

    route.append(start)
    route.reverse()

    return route, travel_times[destination]

if __name__ == "__main__":
    connections = load_travel_times("data/tubedata.csv")

    with open("data/stations.json", "r", encoding="utf-8") as file:
        underground = json.load(file)

    network = build_graph(underground)

    valid_connections = [
        (station_a, station_b, line, minutes)
        for station_a, station_b, line, minutes in connections
        if station_b in network.get(station_a, [])
    ]

    weighted_network = build_weighted_graph(valid_connections)

    corrections = load_travel_time_corrections("data/travel_time_corrections.csv")

    weighted_network = apply_travel_time_corrections(weighted_network, corrections)

    result = find_fastest_route(weighted_network, "Brixton", "Covent Garden")

    if result is None:
        print("No route found.")
    else:
        route, minutes = result

        print("\nFastest route:")
        print(" -> ".join(route))
        print("Estimated journey time:", minutes, "minutes")
