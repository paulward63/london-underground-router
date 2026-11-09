import csv
import json

from graph import build_graph
from inspect_travel_times import (
    station_name_mapping,
    bank_monument_mapping,
    shepherds_bush_mapping,
)

def load_travel_times(filename):
    travel_times = []

    with open(filename, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file, skipinitialspace=True)

        for row in reader:
            if len(row) != 6:
                print("Skipping malformed record:", row)
                continue

            station_a = row[0].strip()
            station_b = row[1].strip()

            station_a = station_name_mapping.get(station_a, station_a)
            station_b = station_name_mapping.get(station_b, station_b)

            line = row[2]

            if line in bank_monument_mapping:
                if station_a == "Bank/Monument":
                    station_a = bank_monument_mapping[line]

                if station_b == "Bank/Monument":
                    station_b = bank_monument_mapping[line]

            if line in shepherds_bush_mapping:
                if station_a == "Shepherd's Bush":
                    station_a = shepherds_bush_mapping[line]

                if station_b == "Shepherd's Bush":
                    station_b = shepherds_bush_mapping[line]

            minutes = int(row[3])

            if minutes <= 0:
                print("Invalid journey time:", row)
                continue

            travel_times.append((station_a, station_b, line, minutes))

    return travel_times

def build_weighted_graph(connections):
    weighted_graph = {}

    for station_a, station_b, line, minutes in connections:
        if station_a not in weighted_graph:
            weighted_graph[station_a] = {}

        if station_b not in weighted_graph:
            weighted_graph[station_b] = {}

        weighted_graph[station_a][station_b] = minutes
        weighted_graph[station_b][station_a] = minutes

    return weighted_graph


def load_travel_time_corrections(filename):
    corrections = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            corrections.append(row)

    return corrections

def validate_correction(correction):
    minutes_text = correction["minutes"].strip()

    if minutes_text == "":
        return False

    try:
        minutes = int(minutes_text)
    except ValueError:
        return False

    return minutes > 0


def apply_travel_time_corrections(weighted_graph, corrections):
    for correction in corrections:
        if not validate_correction(correction):
            continue

        station_a = correction["station_a"].strip()
        station_b = correction["station_b"].strip()
        minutes = int(correction["minutes"].strip())

        if station_a not in weighted_graph:
            weighted_graph[station_a] = {}

        if station_b not in weighted_graph:
            weighted_graph[station_b] = {}

        if station_b not in weighted_graph[station_a]:
            weighted_graph[station_a][station_b] = minutes

        if station_a not in weighted_graph[station_b]:
            weighted_graph[station_b][station_a] = minutes

    return weighted_graph

if __name__ == "__main__":
    travel_times = load_travel_times("data/tubedata.csv")

    with open("data/stations.json", "r", encoding="utf-8") as file:
        underground = json.load(file)

    network = build_graph(underground)

    print("Stations in our network:", len(network))

    print("Valid travel-time records:", len(travel_times))
    print("First record:", travel_times[0])

    for record in travel_times:
        if "Earl's Court" in record:
            print("Corrected station record:", record)

    print("\nChecking Bank and Monument connections:")

    for record in travel_times:
        if "Bank" in record or "Monument" in record:
            print(record)

    print("\nChecking Shepherd's Bush connections:")

    for record in travel_times:
        if "Shepherd's Bush" in record or "Shepherd's Bush Market" in record:
            print(record)

    print("\nChecking historical connections:")

    valid_connections = []
    invalid_connections = []

    for station_a, station_b, line, minutes in travel_times:
        if station_b not in network.get(station_a, []):
            invalid_connections.append((station_a, station_b, line, minutes))
            print("Connection not found:", station_a, "->", station_b, line)
        else:
            valid_connections.append((station_a, station_b, line, minutes))

    print("\nValid connections:", len(valid_connections))
    print("Unmatched connections:", len(invalid_connections))

    weighted_network = build_weighted_graph(valid_connections)

    print("\nWeighted graph test:")
    print(weighted_network["Harrow & Wealdstone"])

    print("\nGreen Park connections:")
    print(weighted_network["Green Park"])

    print("\nTesting both directions:")
    print("Green Park to Hyde Park Corner:", weighted_network["Green Park"]["Hyde Park Corner"])
    print("Hyde Park Corner to Green Park:", weighted_network["Hyde Park Corner"]["Green Park"])

    print("\nWeighted graph coverage:")
    print("Stations with travel-time data:", len(weighted_network))

    missing_stations = set(network.keys()) - set(weighted_network.keys())

    print("Stations missing travel-time data:", len(missing_stations))

    for station in sorted(missing_stations):
        print("Missing:", station)

    total_connections = (
        sum(len(neighbours) for neighbours in weighted_network.values()) // 2
    )

    print("\nTotal weighted connections:", total_connections)

    print("\nConnections missing travel times:")

    missing_connections = set()

    for station_a, neighbours in network.items():
        for station_b in neighbours:
            if station_b not in weighted_network.get(station_a, {}):
                connection = tuple(sorted((station_a, station_b)))
                missing_connections.add(connection)

    for station_a, station_b in sorted(missing_connections):
        print(station_a, "->", station_b)

    print("\nTotal missing connections:", len(missing_connections))

    print("\nChecking travel-time corrections:")

    corrections = load_travel_time_corrections("data/travel_time_corrections.csv")

    print("Total corrections:", len(corrections))
    print("First correction:", corrections[0])

    pending_count = 0

    for correction in corrections:
        if correction["minutes"].strip() == "":
            pending_count += 1

    print("Corrections awaiting journey times:", pending_count)

    print("\nValidating travel-time corrections:")

    valid_count = 0
    invalid_count = 0

    for correction in corrections:
        if validate_correction(correction):
            valid_count += 1
            print("Valid:", correction["station_a"], "->", correction["station_b"])
        else:
            invalid_count += 1
            print(
                "Pending or invalid:",
                correction["station_a"],
                "->",
                correction["station_b"],
            )

    print("\nValid corrections:", valid_count)
    print("Pending or invalid corrections:", invalid_count)


    print("\nApplying travel-time corrections:")

    weighted_network = apply_travel_time_corrections(
        weighted_network, corrections
    )

    total_connections = sum(
        len(neighbours)
        for neighbours in weighted_network.values()
    ) // 2

    print("Stations in weighted network:", len(weighted_network))
    print("Total weighted connections:", total_connections)

    print("\nTesting corrected connections:")

    print(
        "Amersham to Chalfont & Latimer:",
        weighted_network["Amersham"]["Chalfont & Latimer"],
        "minutes"
    )

    print(
        "Battersea Power Station to Nine Elms:",
        weighted_network["Battersea Power Station"]["Nine Elms"],
        "minutes"
    )
