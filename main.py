import argparse

from toonga import collectors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play with api')
    parser.add_argument('--search', type=str, nargs='+',
                        help='search for equivalent names for the entry')

    args = parser.parse_args()

    search = " ".join(args.search)
    print("Searching for:", search)
    for cl in collectors.search_clients:
        c = cl()
        some_series = c.search_series(search)
        if not some_series:
            print("Did not find anything on", c.name)
            continue
        series = some_series[0]
        c.get_series(series)
        print(f"{c.name}: for {series.name}")
        if not series.details or not series.details.other_titles:
            print("  Nothing")
            continue
        for title in series.details.other_titles:
            print(f"  {title}")
