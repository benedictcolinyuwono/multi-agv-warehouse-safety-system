# sims/agv_queue_numeric.py
from dataclasses import dataclass
from typing import List, Set

@dataclass
class AGV:
    id: int
    pos: int      # current cell index on a 1D lane
    goal: int     # last cell index to reach

def occupied_cells(agvs: List[AGV]) -> Set[int]:
    return {a.pos for a in agvs}

def step_grid(agvs: List[AGV], reservations: Set[int]) -> List[AGV]:
    """Advance AGVs by one cell if their next cell was reserved this tick."""
    moved = []
    for a in agvs:
        nxt = a.pos + 1
        if nxt in reservations:
            a = AGV(a.id, nxt, a.goal)
        moved.append(a)
    return moved