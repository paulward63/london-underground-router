def display_route(route):
    print("\nYour journey:")

    for number, station in enumerate(route, start=1):
        print(f"{number}. {station}")

    print(f"\nStops travelled: {len(route) - 1}")
    