from dataclasses import dataclass


@dataclass
class User:
    pfp: str
    name: str
    completed: int
    unique: int
