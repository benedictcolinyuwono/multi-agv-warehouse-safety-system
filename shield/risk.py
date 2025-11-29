import math

# 1D collision risk functions
def time_to_collision(ego_x, ego_v, lead_x, lead_v, epsilon=1e-6):
    gap = lead_x - ego_x
    closing_speed = ego_v - lead_v
    if closing_speed <= 0:
        return math.inf
    ttc_seconds = gap / max(closing_speed, epsilon)
    return max(ttc_seconds, 0.0)

def time_headway(ego_v, gap_m, epsilon=1e-6):
    if abs(ego_v) < epsilon:
        return math.inf
    return gap_m / max(ego_v, epsilon)

def assess_collision_risk(state):
    WARNING_THRESHOLD = 2.0
    CRITICAL_THRESHOLD = 1.0
    ttc = time_to_collision(
        state["ego_x"], state["ego_v"],
        state["lead_x"], state["lead_v"]
    )
    headway = time_headway(state["ego_v"], state["gap_m"])
    return {
        "ttc": ttc,
        "headway": headway,
        "margin_low": (ttc < WARNING_THRESHOLD or headway < WARNING_THRESHOLD),
        "violation_predicted": (ttc < CRITICAL_THRESHOLD or headway < CRITICAL_THRESHOLD),
    }


# 2D collision risk functions
def time_to_collision_2d(ego_x, ego_y, ego_vx, ego_vy, other_x, other_y, other_vx=0.0, other_vy=0.0, safety_radius=1.0, epsilon=1e-6):
    delta_x = other_x - ego_x
    delta_y = other_y - ego_y
    gap = math.sqrt(delta_x * delta_x + delta_y * delta_y)
    
    effective_gap = gap - (2.0 * safety_radius)
    
    if effective_gap <= 0.0:
        return 0.0
    
    relative_vx = ego_vx - other_vx
    relative_vy = ego_vy - other_vy
    
    my_speed = math.sqrt(relative_vx * relative_vx + relative_vy * relative_vy)
    
    if my_speed < epsilon:
        return math.inf
    
    # Dot product: project velocity onto gap vector
    closing_speed = (relative_vx * delta_x + relative_vy * delta_y) / max(gap, epsilon)
    
    if closing_speed <= 0.0:
        return math.inf
    
    return effective_gap / closing_speed


def time_headway_2d(ego_vx, ego_vy, gap_m, epsilon=1e-6):
    ego_speed = math.sqrt(ego_vx * ego_vx + ego_vy * ego_vy)
    
    if ego_speed < epsilon:
        return math.inf
    
    return gap_m / max(ego_speed, epsilon)


def assess_collision_risk_2d(ego_x, ego_y, ego_vx, ego_vy, other_x, other_y, other_vx=0.0, other_vy=0.0, safety_radius=1.0):
    WARNING_THRESHOLD = 2.0
    CRITICAL_THRESHOLD = 1.0
    
    delta_x = other_x - ego_x
    delta_y = other_y - ego_y
    gap_m = math.sqrt(delta_x * delta_x + delta_y * delta_y)
    
    ttc = time_to_collision_2d(ego_x, ego_y, ego_vx, ego_vy, other_x, other_y, other_vx, other_vy, safety_radius)
    headway = time_headway_2d(ego_vx, ego_vy, gap_m)
    
    return {
        "ttc": ttc,
        "headway": headway,
        "gap_m": gap_m,
        "margin_low": (ttc < WARNING_THRESHOLD or headway < WARNING_THRESHOLD),
        "violation_predicted": (ttc < CRITICAL_THRESHOLD or headway < CRITICAL_THRESHOLD),
    }