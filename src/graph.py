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
