# toonga-info
Get basic information from common sites about manga / manwha / webtoons

Mostly made to get alternatives titles for a manga /webtoon and/or latest chapter available.

Currently the info are gathered for each supported website:
* name
* last chapters
* summary
* other titles

# Features

Supported websites
* MangaUpdate / BakaUpdate 
* Mangadex
* tapas
* tappytoon
* webtoon

# Examples

````python
from toonga import collectors

c = collectors.MangaUpdateClient()

# Let's look for a series where we know only the name
some_series = c.search_series("queen")  # Return a list of Series

# Taking the best one
series = some_series[0]

# Query all the details we can
series = c.get_series(series)

print("Last Chapters", series.details.chapters)
print("Alternative titles", series.details.other_titles)
````

Clients:

````python
from toonga import collectors

c = collectors.MangaUpdateClient()
d = collectors.MangaDexClient()
t = collectors.TapasClient()
tt = collectors.TappyToonClient()
w = collectors.WebToonClient()
````

See `main.py` from some examples

# Install

Run `pip install .` in this folder
