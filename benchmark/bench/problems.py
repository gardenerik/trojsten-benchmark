from dataclasses import dataclass


@dataclass
class Problem:
    id: str
    competition: str
    problem: str
    solution: str
    difficulty: int
