from graph import find_connection_lines

def display_route(route):
    print("\nYour journey:")

    for number, station in enumerate(route, start=1):
        print(f"{number}. {station}")

    print(f"\nStops travelled: {len(route) - 1}")


def display_journey_lines(underground, route):
    print("\nJourney line instructions:")

    if len(route) == 1:
        print("You are already at your destination!")
        return

    current_line = None

    for i in range(len(route) - 1):
        station_a = route[i]
        station_b = route[i + 1]

        lines = find_connection_lines(underground, station_a, station_b)
        continuing_lines = set()

        if i + 2 < len(route):
            next_station = route[i + 2]
            next_lines = find_connection_lines(
            underground, station_b, next_station
        )

            continuing_lines = set(lines) & set(next_lines)
        #    print("DEBUG - Continuing lines:", continuing_lines)

        if lines:
            if current_line is None:
                if continuing_lines:
                    current_line = next(
                        line for line in lines if line in continuing_lines
                    )
                else:
                    current_line = lines[0]

                print("Board the", current_line, "Line at", station_a)

            elif current_line not in lines:
                print("Travel to", station_a)
                current_line = lines[0]
                print("Change to the", current_line, "Line at", station_a)

        #    print(station_a, "->", station_b, ":", lines[0], "Line")

    if len(route) > 1:
        print("Travel to", route[-1])


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
