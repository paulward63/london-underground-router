def find_station_lines(underground, station_name):
    lines = []

    for line_name, stations in underground.items():
        if station_name in stations:
            lines.append(line_name)

    return lines


def find_common_lines(start_lines, destination_lines):

    common_lines = []

    for line in start_lines:
        if line in destination_lines:
            common_lines.append(line)

    return common_lines


def find_interchanges(underground, first_line, second_line):
    interchanges = []

    for station in underground[first_line]:
        if station in underground[second_line]:
            interchanges.append(station)

    return interchanges
