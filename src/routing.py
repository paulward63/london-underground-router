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
