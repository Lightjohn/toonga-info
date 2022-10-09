from .mangadex import Client as MangaDexClient
from .mangaupdate import Client as MangaUpdateClient
from .tapas import Client as TapasClient
from .tappytoon import Client as TappyToonClient
from .webtoon import Client as WebToonClient

search_clients = [MangaDexClient, MangaUpdateClient]
all_clients = [MangaDexClient, MangaUpdateClient, TapasClient, TappyToonClient, WebToonClient]
