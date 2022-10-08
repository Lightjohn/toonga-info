import argparse
import json
import sys
import time

from unidecode import unidecode

from toonga import collectors


def search_from_string(search_query):
    print("Searching for:", search_query)
    for cl in collectors.search_clients:
        c = cl()
        some_series = c.search_series(search_query)
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


def search_from_json(json_path):
    with open(json_path) as f:
        data = json.load(f)

    c = [c() for c in collectors.all_clients]
    for query in data:
        title = unidecode(query["title"])
        last_chapter = query["last_chapter"]
        last_chapter_collector = []
        try:
            for collector in c:
                some_series = collector.search_series(title)
                if not some_series:
                    continue
                series = some_series[0]  # First is the closest to what we want
                chapters = collector.get_chapters(series)
                if chapters:
                    last_chapter_collector.append((chapters[0].num, collector.name))
            if not last_chapter_collector:
                print(title, "Could not be found anywhere")
            is_okay = "UP TO DATE" if max(
                [float(i) for i, j in last_chapter_collector]) <= last_chapter else "CAN BE UPDATED"
            print(title + ":", is_okay)
            print("  Existing:", last_chapter, ", ".join(f"{j}: {i}" for i, j in last_chapter_collector))
            time.sleep(2)   # Be kind
        except Exception as e:
            print("Error happened")
            print(title, collector.name)
            print(e)
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play with api')
    parser.add_argument('--search', type=str, nargs='+',
                        help='search for equivalent names for the entry')
    parser.add_argument('--json', type=str,
                        help='path to json files')

    args = parser.parse_args()

    if args.search:
        search_from_string(" ".join(args.search))
        sys.exit(0)
    if args.json:
        search_from_json(args.json)
        sys.exit(0)
