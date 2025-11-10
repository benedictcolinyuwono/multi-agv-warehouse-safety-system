# scripts/run_numeric_agv.py
import csv
from sims.agv_queue_numeric import AGV, step_grid, occupied_cells

def run(output_csv="data/logs/agv_queue_numeric.csv",
        cells=12, steps=40, junction_cell=6):
    """
    1D lane of 'cells' with a single junction at J.
    Two AGVs move toward the end; rules:
      - headway >= 1 empty cell (i.e., gap_cells >= 1)
      - don't block the box: only enter junction cell J if J+1 is free
    """
    J = junction_cell
    agvs = [AGV(id=0, pos=0, goal=cells-1),   # follower
            AGV(id=1, pos=2, goal=cells-1)]  # leader (ahead by 2 cells)

    with open(output_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t","a0_pos","a1_pos","headway_cells","entered_junction"])

        for t in range(steps):
            occ = occupied_cells(agvs)
            gap_cells = agvs[1].pos - agvs[0].pos
            headway_cells = gap_cells if gap_cells > 0 else 0

            reservations = set()

            # Leader (AGV1)
            next1 = agvs[1].pos + 1
            enter1_ok = True
            if next1 == J:                       # entering junction?
                enter1_ok = (J + 1) not in occ   # exit must be free
            if enter1_ok:
                reservations.add(next1)

            # Follower (AGV0) — keep >=1 empty cell between them
            next0 = agvs[0].pos + 1
            if headway_cells >= 2:               # at least one empty cell in between
                enter0_ok = True
                if next0 == J:
                    enter0_ok = (J + 1) not in occ
                if enter0_ok:
                    reservations.add(next0)

            before_enter = (agvs[0].pos == J-1) or (agvs[1].pos == J-1)
            agvs = step_grid(agvs, reservations)
            after_enter = (agvs[0].pos == J) or (agvs[1].pos == J)

            w.writerow([t, agvs[0].pos, agvs[1].pos, headway_cells,
                        int(after_enter and not before_enter)])

if __name__ == "__main__":
    run()
    print("Wrote data/logs/agv_queue_numeric.csv")