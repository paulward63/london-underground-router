from graph import find_connection_lines
import heapq

def calculate_route(stations, start_station, destination):

    start_index = stations.index(start_station)
    destination_index = stations.index(destination)

    if start_index < destination_index:
        route = stations[start_index : destination_index + 1]

    elif start_index > destination_index:
        route = stations[destination_index : start_index + 1]
        route.reverse()

    else:
        route = [start_station]

    return route


def find_best_interchange(
    underground, start_station, destination, interchanges, start_line, destination_line
):

    best_route = None
    best_interchange = None

    for interchange in interchanges:

        first_route = calculate_route(
            underground[start_line], start_station, interchange
        )

        second_route = calculate_route(
            underground[destination_line], interchange, destination
        )

        complete_route = first_route + second_route[1:]

        if best_route is None or len(complete_route) < len(best_route):
            best_route = complete_route
            best_interchange = interchange

    return best_route, best_interchange


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

def count_interchanges(underground, route):
    previous_lines = set()
    interchange_count = 0

    for i in range(len(route) - 1):
        station_a = route[i]
        station_b = route[i + 1]

        lines = set(find_connection_lines(underground, station_a, station_b))

        if previous_lines:
            common_lines = previous_lines & lines

            if common_lines:
                previous_lines = common_lines
            else:

                interchange_count += 1
                previous_lines = lines

        else:
            previous_lines = lines

    return interchange_count


def find_fewest_interchanges_route(underground, network, start_station, destination):
    queue = []

    best_cost = {
        (start_station, None): (0, 0)
    }

    heapq.heappush(queue, (0, 0, start_station, None, [start_station]))

    while queue:
        interchanges, stops, current_station, current_line, route = heapq.heappop(queue)

        state = (current_station, current_line)
        cost = (interchanges, stops)

        if cost > best_cost[state]:
            continue

        if current_station == destination:
            return route

        for next_station in network[current_station]:
        #    print("Exploring:", current_station, "->", next_station)

            available_lines = find_connection_lines(
                underground, current_station, next_station
            )

            for line in available_lines:
                new_interchanges = interchanges

                if current_line is not None and current_line != line:
                    new_interchanges += 1

                new_stops = stops + 1

                new_route = route + [next_station]

                state = (next_station, line)
                new_cost = (new_interchanges, new_stops)

                if state in best_cost and new_cost >= best_cost[state]:
                    continue

                best_cost[state] = new_cost

                heapq.heappush(
                    queue,
                    (new_interchanges, new_stops, next_station, line, new_route)
                )
    return None
