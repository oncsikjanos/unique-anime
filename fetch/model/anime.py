from dataclasses import dataclass


@dataclass
class Anime:
    id: int
    title: str
    media: str
    picture: str
    rating: float
    episodes: int
    episode_duration: int
