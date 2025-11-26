import csv
from sims.agv_queue_numeric import AGV, step_with_reservations, get_occupied_cells

NUM_CELLS = 12
NUM_STEPS = 40
JUNCTION_CELL = 6
MIN_HEADWAY_CELLS = 1


def run(output_csv="data/logs/agv_queue_numeric.csv",
        cells=NUM_CELLS, steps=NUM_STEPS, junction_cell=JUNCTION_CELL):
    J = junction_cell
    
    agvs = [
        AGV(id=0, pos=0, goal=cells-1),
        AGV(id=1, pos=2, goal=cells-1)
    ]
    
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["t", "a0_pos", "a1_pos", "headway_cells", "entered_junction"])
        
        for t in range(steps):
            occ = get_occupied_cells(agvs)
            gap_cells = agvs[1].pos - agvs[0].pos
            headway_cells = max(gap_cells, 0)
            
            reservations = set()
            
            next_leader = agvs[1].pos + 1
            can_enter = True
            if next_leader == J:
                can_enter = (J + 1) not in occ
            if can_enter:
                reservations.add(next_leader)
            
            next_follower = agvs[0].pos + 1
            if headway_cells >= MIN_HEADWAY_CELLS + 1:
                can_enter = True
                if next_follower == J:
                    can_enter = (J + 1) not in occ
                if can_enter:
                    reservations.add(next_follower)
            
            before = (agvs[0].pos == J-1) or (agvs[1].pos == J-1)
            agvs = step_with_reservations(agvs, reservations)
            after = (agvs[0].pos == J) or (agvs[1].pos == J)
            
            writer.writerow([
                t, agvs[0].pos, agvs[1].pos, headway_cells,
                int(after and not before)
            ])
    
    print(f"Simulation complete: {output_csv}")


if __name__ == "__main__":
    run()
    print("Wrote data/logs/agv_queue_numeric.csv")