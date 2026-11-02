def build_graph(underground):
    graph = {}

    for line_name, stations in underground.items():

        if isinstance(stations, dict):
            station_lists = stations.values()
        else:
            station_lists = [stations]

        for station_list in station_lists:

            for i in range(len(station_list) - 1):
                station_a = station_list[i]
                station_b = station_list[i + 1]

                if station_a not in graph:
                    graph[station_a] = []

                if station_b not in graph:
                    graph[station_b] = []

                if station_b not in graph[station_a]:
                    graph[station_a].append(station_b)

                if station_a not in graph[station_b]:
                    graph[station_b].append(station_a)

    return graph
