import csv
import json
from graph import build_graph

station_name_mapping = {
    "Heathrow Terminal 3": "Heathrow Terminals 2 & 3",
    "King's Cross St. Pancras": "King's Cross St Pancras",
    "St. James' Park": "St. James's Park",
    "Earls' Court": "Earl's Court",
    "Olympia": "Kensington (Olympia)",
}

bank_monument_mapping = {
    "Central": "Bank",
    "Northern": "Bank",
    "Waterloo & City": "Bank",
    "Circle": "Monument",
    "District": "Monument",
}

shepherds_bush_mapping = {
    "Hammersmith & City": "Shepherd's Bush Market",
}

with open("data/stations.json", "r", encoding="utf-8") as file:
    underground = json.load(file)

    print("Underground lines loaded:", len(underground))

    network = build_graph(underground)

    print("Unique station names:", len(network))

with open("data/tubedata.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.reader(file, skipinitialspace=True)

    line_counts = {}

    csv_stations = set()

    for row in reader:
        if len(row) != 6:
            print("Skipping malformed CSV record:", row)
            continue

        line_name = row[2]

        station_a = row[0].strip()
        station_b = row[1].strip()

        station_a = station_name_mapping.get(station_a, station_a)
        station_b = station_name_mapping.get(station_b, station_b)

        if line_name in bank_monument_mapping:
            if station_a == "Bank/Monument":
                station_a = bank_monument_mapping[line_name]

            if station_b == "Bank/Monument":
                station_b = bank_monument_mapping[line_name]

        # Handle the historical Shepherd's Bush station name
        if line_name in shepherds_bush_mapping:
            if station_a == "Shepherd's Bush":
                station_a = shepherds_bush_mapping[line_name]

            if station_b == "Shepherd's Bush":
                station_b = shepherds_bush_mapping[line_name]

        csv_stations.add(station_a)
        csv_stations.add(station_b)

        if line_name in ("2", '3"""'):
            print("Unusual CSV record:", row)

        if line_name not in line_counts:
            line_counts[line_name] = 0

        line_counts[line_name] += 1

    print("\nUnderground connections by line:")

    for line, count in sorted(line_counts.items()):
        print(f"{line}: {count} connections")

    print("\nUnique CSV station names:", len(csv_stations))

missing_from_network = csv_stations - set(network.keys())

print("\nCSV stations not found in our network:")

for station in sorted(missing_from_network):
    print(station)

missing_from_csv = set(network.keys()) - csv_stations

print("\nNetwork stations not found in CSV:")

for station in sorted(missing_from_csv):
    print(station)

# print("\nChecking Earl's Court station names:")

# for station in sorted(csv_stations):
#     if "Court" in station:
#         print("CSV:", repr(station))

# for station in sorted(network.keys()):
#     if "Court" in station:
#         print("JSON:", repr(station))
