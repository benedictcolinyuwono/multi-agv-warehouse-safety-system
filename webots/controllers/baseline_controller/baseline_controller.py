from controller import Supervisor
import math
import random
import sys
from pathlib import Path

# Add repo root to Python path so we can import shield/ modules
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from waypoints import warehouse_waypoints
from path_planner import get_path_planner
from shield.risk import assess_collision_risk_2d
from shield.supervisor import supervise_commands

robot = Supervisor()
timestep = int(robot.getBasicTimeStep())
robot_name = robot.getName()

front_right_motor = robot.getDevice('front_right_wheel_joint')
front_left_motor = robot.getDevice('front_left_wheel_joint')
back_right_motor = robot.getDevice('back_right_wheel_joint')
back_left_motor = robot.getDevice('back_left_wheel_joint')

front_right_motor.setPosition(float('inf'))
front_left_motor.setPosition(float('inf'))
back_right_motor.setPosition(float('inf'))
back_left_motor.setPosition(float('inf'))

front_right_motor.setVelocity(0.0)
front_left_motor.setVelocity(0.0)
back_right_motor.setVelocity(0.0)
back_left_motor.setVelocity(0.0)

gps = robot.getDevice('gps')
gps.enable(timestep)

compass = robot.getDevice('compass')
compass.enable(timestep)

WHEEL_RADIUS = 0.125
AXLE_LENGTH = 0.55
WAYPOINT_THRESHOLD = 1.0

K_THETA = 2.0
MAX_V = 1.0
MAX_W = 1.5

STARTUP_HOLD_STEPS = 5
INITIAL_DELAY_NOT_AT_HOME = 5.0
HOME_DETECTION_THRESHOLD = 1.0

TURN_MODE_ENTER_THRESHOLD = 0.35
TURN_MODE_EXIT_THRESHOLD = 0.10

DWELL_TIME = 5.0

QUEUE_OCCUPANCY_THRESHOLD = 1.0
AISLE_OCCUPANCY_THRESHOLD = 2.5
TOP_TURN_WAIT_THRESHOLD = 1.0
BOTTOM_WAIT_IGNORE_THRESHOLD = 4.3
TOP_QUEUE_IGNORE_THRESHOLD = 4.3

# Level C shield settings
SHIELD_SAFETY_RADIUS = 0.5
SHIELD_NEIGHBOR_RADIUS = 5.0
SHIELD_MODE_LOG_EVERY = 20

# Bottom merge-yield settings
AISLE_EXIT_REQUEST_THRESHOLD = 2.5
BOTTOM_MERGE_YIELD_THRESHOLD = 2.5

HOME_GROUP = "row_a_aisle_1_top_turn"
HOME_INDEX = 0

GO_TO_TARGET = "GO_TO_TARGET"
RETURN_HOME = "RETURN_HOME"
DWELL = "DWELL"

VALID_TASKS = []
for aisle_num in range(2, 18):
    for wp_idx in range(1, 7):
        VALID_TASKS.append((f"row_a_aisle_{aisle_num}", wp_idx))

AGV_DEF_NAMES = [f"AGV_{i}" for i in range(1, 9)]


def normalize_angle(angle):
    while angle > math.pi:
        angle -= 2.0 * math.pi
    while angle < -math.pi:
        angle += 2.0 * math.pi
    return angle


def stop_motors():
    front_right_motor.setVelocity(0.0)
    front_left_motor.setVelocity(0.0)
    back_right_motor.setVelocity(0.0)
    back_left_motor.setVelocity(0.0)


def pick_next_task(previous_task=None):
    return ("row_a_aisle_3", 2)
    # candidates = VALID_TASKS[:]
    # if previous_task in candidates and len(candidates) > 1:
    #     candidates.remove(previous_task)
    # return random.choice(candidates)


def get_other_agv_positions():
    positions = []

    for def_name in AGV_DEF_NAMES:
        node = robot.getFromDef(def_name)
        if node is None:
            continue

        if def_name == robot_name:
            continue

        trans_field = node.getField("translation")
        if trans_field is None:
            continue

        tx, ty, tz = trans_field.getSFVec3f()
        positions.append((def_name, tx, ty))

    return positions


def point_is_occupied_by_other_agv(target_x, target_y, threshold=QUEUE_OCCUPANCY_THRESHOLD):
    others = get_other_agv_positions()

    for other_name, ox, oy in others:
        d = math.hypot(ox - target_x, oy - target_y)
        if d < threshold:
            return True, other_name

    return False, None


def is_aisle_1_queue_or_home_target(target_x, target_y):
    aisle1_points = warehouse_waypoints["row_a_aisle_1"]
    home_point = warehouse_waypoints["row_a_aisle_1_top_turn"][0]

    all_queue_points = aisle1_points + [home_point]

    for px, py in all_queue_points:
        if math.hypot(target_x - px, target_y - py) < 0.5:
            return True

    return False


def is_home_target(target_x, target_y, threshold=0.5):
    home_x, home_y = warehouse_waypoints[HOME_GROUP][HOME_INDEX]
    return math.hypot(target_x - home_x, target_y - home_y) < threshold


def get_task_aisle_name_from_task(task):
    if task is None:
        return None
    return task[0]


def get_first_point_for_aisle(aisle_name):
    return warehouse_waypoints[aisle_name][0]


def target_matches_point(target_x, target_y, point_x, point_y, threshold=TOP_TURN_WAIT_THRESHOLD):
    return math.hypot(target_x - point_x, target_y - point_y) < threshold


def get_bottom_turn_point_for_aisle(aisle_name):
    return warehouse_waypoints[f"{aisle_name}_bottom_turn"][0]


def get_bottom_wait_point_for_aisle(aisle_name):
    return warehouse_waypoints[f"{aisle_name}_bottom_wait"][0]


def get_top_wait_point_for_aisle(aisle_name):
    return warehouse_waypoints[f"{aisle_name}_top_wait"][0]


def get_top_turn_point_for_aisle(aisle_name):
    return warehouse_waypoints[f"{aisle_name}_top_turn"][0]


def is_other_agv_at_bottom_wait_of_aisle(other_x, other_y, aisle_name, threshold=BOTTOM_WAIT_IGNORE_THRESHOLD):
    bwx, bwy = get_bottom_wait_point_for_aisle(aisle_name)
    return math.hypot(other_x - bwx, other_y - bwy) < threshold


def is_other_agv_at_top_wait_of_aisle(other_x, other_y, aisle_name, threshold=TOP_QUEUE_IGNORE_THRESHOLD):
    twx, twy = get_top_wait_point_for_aisle(aisle_name)
    return math.hypot(other_x - twx, other_y - twy) < threshold


def is_other_agv_at_top_turn_of_aisle(other_x, other_y, aisle_name, threshold=TOP_QUEUE_IGNORE_THRESHOLD):
    ttx, tty = get_top_turn_point_for_aisle(aisle_name)
    return math.hypot(other_x - ttx, other_y - tty) < threshold


def other_agv_occupies_aisle(aisle_name, threshold=AISLE_OCCUPANCY_THRESHOLD):
    aisle_points = warehouse_waypoints[aisle_name]

    for other_name, ox, oy in get_other_agv_positions():
        if is_other_agv_at_bottom_wait_of_aisle(ox, oy, aisle_name):
            continue
        if is_other_agv_at_top_wait_of_aisle(ox, oy, aisle_name):
            continue
        if is_other_agv_at_top_turn_of_aisle(ox, oy, aisle_name):
            continue

        for px, py in aisle_points:
            if math.hypot(ox - px, oy - py) < threshold:
                return True, other_name

    return False, None


def other_agv_occupies_bottom_turn(aisle_name, threshold=AISLE_OCCUPANCY_THRESHOLD):
    bx, by = get_bottom_turn_point_for_aisle(aisle_name)

    for other_name, ox, oy in get_other_agv_positions():
        if is_other_agv_at_bottom_wait_of_aisle(ox, oy, aisle_name):
            continue

        if math.hypot(ox - bx, oy - by) < threshold:
            return True, other_name

    return False, None


def is_top_queue_target(target_x, target_y):
    for aisle_num in range(2, 18):
        aisle_name = f"row_a_aisle_{aisle_num}"
        top_wait = get_top_wait_point_for_aisle(aisle_name)
        top_turn = get_top_turn_point_for_aisle(aisle_name)

        if math.hypot(target_x - top_wait[0], target_y - top_wait[1]) < 1.0:
            return True, aisle_name

        if math.hypot(target_x - top_turn[0], target_y - top_turn[1]) < 1.0:
            return True, aisle_name

    return False, None


def estimate_ego_velocity_components(linear_velocity, heading_rad):
    vx = linear_velocity * math.cos(heading_rad)
    vy = linear_velocity * math.sin(heading_rad)
    return vx, vy


def get_most_critical_risk(current_x, current_y, ego_vx, ego_vy):
    best_risk = None
    best_other = None

    for other_name, ox, oy in get_other_agv_positions():
        gap = math.hypot(ox - current_x, oy - current_y)

        if gap > SHIELD_NEIGHBOR_RADIUS:
            continue

        risk = assess_collision_risk_2d(
            ego_x=current_x,
            ego_y=current_y,
            ego_vx=ego_vx,
            ego_vy=ego_vy,
            other_x=ox,
            other_y=oy,
            other_vx=0.0,
            other_vy=0.0,
            safety_radius=SHIELD_SAFETY_RADIUS,
        )

        if best_risk is None:
            best_risk = risk
            best_other = other_name
        else:
            current_score = min(best_risk["ttc"], best_risk["headway"])
            new_score = min(risk["ttc"], risk["headway"])

            if new_score < current_score:
                best_risk = risk
                best_other = other_name

    return best_other, best_risk


def is_near_aisle_exit(current_x, current_y, aisle_name, threshold=AISLE_EXIT_REQUEST_THRESHOLD):
    aisle_points = warehouse_waypoints[aisle_name]
    exit_x, exit_y = aisle_points[-1]
    return math.hypot(current_x - exit_x, current_y - exit_y) < threshold


def get_aisle_exit_requests():
    requests = []

    for aisle_num in range(2, 18):
        aisle_name = f"row_a_aisle_{aisle_num}"
        aisle_points = warehouse_waypoints[aisle_name]
        exit_x, exit_y = aisle_points[-1]

        for other_name, ox, oy in get_other_agv_positions():
            if math.hypot(ox - exit_x, oy - exit_y) < AISLE_EXIT_REQUEST_THRESHOLD:
                requests.append((aisle_name, other_name))

    return requests


def is_near_bottom_merge_zone(current_x, current_y, aisle_name, threshold=BOTTOM_MERGE_YIELD_THRESHOLD):
    bottom_turn_x, bottom_turn_y = get_bottom_turn_point_for_aisle(aisle_name)
    bottom_wait_x, bottom_wait_y = get_bottom_wait_point_for_aisle(aisle_name)

    near_bottom_turn = math.hypot(current_x - bottom_turn_x, current_y - bottom_turn_y) < threshold
    near_bottom_wait = math.hypot(current_x - bottom_wait_x, current_y - bottom_wait_y) < threshold

    return near_bottom_turn or near_bottom_wait


robot_planner = get_path_planner()

current_waypoint_index = 0
step_count = 0
turn_mode = True

mode = RETURN_HOME
current_task = None
previous_task = None

waypoint_path = []
path_initialized = False
printed_start = False

dwell_start_time = None
next_mode_after_dwell = None

initial_delay_checked = False
initial_delay_required = False

home_x, home_y = warehouse_waypoints[HOME_GROUP][HOME_INDEX]


def plan_new_path(current_x, current_y, goal_group, goal_index):
    return robot_planner.find_path(current_x, current_y, goal_group, goal_index)


while robot.step(timestep) != -1:
    step_count += 1

    if step_count <= STARTUP_HOLD_STEPS:
        stop_motors()
        continue

    current_time = robot.getTime()

    gps_values = gps.getValues()
    current_x = gps_values[0]
    current_y = gps_values[1]

    compass_values = compass.getValues()
    current_heading = math.atan2(compass_values[0], compass_values[1])

    if not initial_delay_checked:
        dist_to_home_at_start = math.hypot(current_x - home_x, current_y - home_y)

        if dist_to_home_at_start > HOME_DETECTION_THRESHOLD:
            initial_delay_required = True
            print(f"{robot_name}: not at home on startup, waiting {INITIAL_DELAY_NOT_AT_HOME:.1f}s before moving")
        else:
            initial_delay_required = False
            print(f"{robot_name}: already at home on startup, no initial delay")

        initial_delay_checked = True

    if initial_delay_required and current_time < INITIAL_DELAY_NOT_AT_HOME:
        stop_motors()
        continue

    if mode == DWELL:
        stop_motors()

        if dwell_start_time is None:
            dwell_start_time = current_time

        if current_time - dwell_start_time >= DWELL_TIME:
            dwell_start_time = None

            if next_mode_after_dwell == RETURN_HOME:
                mode = RETURN_HOME
            elif next_mode_after_dwell == GO_TO_TARGET:
                previous_task = current_task
                current_task = pick_next_task(previous_task)
                print(f"{robot_name}: loaded at home, next task is {current_task[0]}[{current_task[1]}]")
                mode = GO_TO_TARGET

            next_mode_after_dwell = None
            path_initialized = False
            waypoint_path = []
            current_waypoint_index = 0
            turn_mode = True

        continue

    if not path_initialized:
        if mode == GO_TO_TARGET:
            if current_task is None:
                print(f"{robot_name}: no task assigned yet")
                stop_motors()
                continue
            goal_group, goal_index = current_task
        else:
            goal_group, goal_index = HOME_GROUP, HOME_INDEX

        waypoint_path = plan_new_path(current_x, current_y, goal_group, goal_index)

        if waypoint_path:
            current_waypoint_index = 0
            turn_mode = True
            if not printed_start:
                print(f"{robot_name}: controller started")
                printed_start = True
            print(f"{robot_name}: mode={mode}, planning to {goal_group}[{goal_index}] with {len(waypoint_path)} points")
        else:
            print(f"{robot_name}: PATH PLANNING FAILED for {goal_group}[{goal_index}]")
            waypoint_path = []

        path_initialized = True

    if not waypoint_path or current_waypoint_index >= len(waypoint_path):
        stop_motors()
        continue

    target_x, target_y = waypoint_path[current_waypoint_index]

    dx = target_x - current_x
    dy = target_y - current_y
    distance_to_waypoint = math.sqrt(dx * dx + dy * dy)

    angle_to_waypoint = math.atan2(dy, dx)
    angle_diff = normalize_angle(angle_to_waypoint - current_heading)

    if distance_to_waypoint < WAYPOINT_THRESHOLD:
        current_waypoint_index += 1

        if current_waypoint_index >= len(waypoint_path):
            stop_motors()

            if mode == GO_TO_TARGET:
                reached_group, reached_index = current_task
                print(f"{robot_name}: reached target {reached_group}[{reached_index}], dwelling before return")
                mode = DWELL
                next_mode_after_dwell = RETURN_HOME
            else:
                print(f"{robot_name}: reached home, dwelling before loading next task")
                mode = DWELL
                next_mode_after_dwell = GO_TO_TARGET

            continue

        continue

    # LEVEL C: aisle 1 queue behaves like corridor spacing now.
    # Only keep hard protection for the actual home/loading point.
    if mode == RETURN_HOME and is_home_target(target_x, target_y):
        occupied, blocking_agv = point_is_occupied_by_other_agv(
            target_x, target_y,
            threshold=QUEUE_OCCUPANCY_THRESHOLD
        )
        if occupied:
            if step_count % 20 == 0:
                print(f"{robot_name}: blocked at home by {blocking_agv}")
            stop_motors()
            continue

    # KEEP: aisle-entry protection
    if mode == GO_TO_TARGET and current_task is not None:
        task_aisle = get_task_aisle_name_from_task(current_task)
        first_x, first_y = get_first_point_for_aisle(task_aisle)

        if target_matches_point(target_x, target_y, first_x, first_y):
            aisle_occupied, aisle_blocker = other_agv_occupies_aisle(task_aisle)
            bottom_turn_occupied, bottom_turn_blocker = other_agv_occupies_bottom_turn(task_aisle)

            if aisle_occupied or bottom_turn_occupied:
                if step_count % 20 == 0:
                    print(
                        f"{robot_name}: blocked from entering {task_aisle}, "
                        f"aisle_occupied={aisle_occupied} ({aisle_blocker}), "
                        f"bottom_turn_occupied={bottom_turn_occupied} ({bottom_turn_blocker})"
                    )
                stop_motors()
                continue

    # LEVEL C STRUCTURAL MERGE RULE:
    # bottom corridor AGVs must leave space if another AGV is near waypoint 8
    # of an aisle and may need to exit first.
    if mode == RETURN_HOME:
        should_yield_bottom_merge = False
        yielding_aisle = None
        yielding_blocker = None

        exit_requests = get_aisle_exit_requests()

        for exit_aisle, exit_blocker in exit_requests:
            if current_task is not None and current_task[0] == exit_aisle:
                if is_near_aisle_exit(current_x, current_y, exit_aisle, threshold=AISLE_EXIT_REQUEST_THRESHOLD):
                    continue

            if is_near_bottom_merge_zone(current_x, current_y, exit_aisle, threshold=BOTTOM_MERGE_YIELD_THRESHOLD):
                should_yield_bottom_merge = True
                yielding_aisle = exit_aisle
                yielding_blocker = exit_blocker
                break

        if should_yield_bottom_merge:
            if step_count % 20 == 0:
                print(
                    f"{robot_name}: yielding on bottom corridor, "
                    f"{yielding_blocker} near exit of {yielding_aisle}"
                )
            stop_motors()
            continue

    angular_velocity = max(-MAX_W, min(MAX_W, K_THETA * angle_diff))

    if turn_mode:
        if abs(angle_diff) < TURN_MODE_EXIT_THRESHOLD:
            turn_mode = False
    else:
        if abs(angle_diff) > TURN_MODE_ENTER_THRESHOLD:
            turn_mode = True

    base_linear_velocity = min(MAX_V, 0.8 * distance_to_waypoint)

    if turn_mode:
        linear_velocity = 0.0
    else:
        heading_scale = max(0.0, math.cos(angle_diff))
        linear_velocity = base_linear_velocity * heading_scale

    shield_mode = "PASS"

    # LEVEL C: SAFETY SHIELD SUPERVISORY LAYER
    if not is_home_target(target_x, target_y):
        ego_vx, ego_vy = estimate_ego_velocity_components(linear_velocity, current_heading)
        blocking_agv, critical_risk = get_most_critical_risk(current_x, current_y, ego_vx, ego_vy)

        if critical_risk is not None:
            shield_state = {
                "ego_x": current_x,
                "ego_y": current_y,
                "ego_vx": ego_vx,
                "ego_vy": ego_vy,
                "v_cap": MAX_V,
            }

            shield_mode, (linear_velocity, angular_velocity) = supervise_commands(
                shield_state,
                (linear_velocity, angular_velocity),
                critical_risk
            )

            if step_count % SHIELD_MODE_LOG_EVERY == 0:
                print(
                    f"{robot_name}: shield_mode={shield_mode}, "
                    f"blocker={blocking_agv}, "
                    f"ttc={critical_risk['ttc']:.2f}, "
                    f"headway={critical_risk['headway']:.2f}, "
                    f"gap={critical_risk['gap_m']:.2f}"
                )

    left_velocity = (linear_velocity - 0.5 * AXLE_LENGTH * angular_velocity) / WHEEL_RADIUS
    right_velocity = (linear_velocity + 0.5 * AXLE_LENGTH * angular_velocity) / WHEEL_RADIUS

    if step_count % 20 == 0:
        print(
            f"{robot_name} | mode={mode} "
            f"pos=({current_x:.2f},{current_y:.2f}) "
            f"target=({target_x:.2f},{target_y:.2f}) "
            f"dist={distance_to_waypoint:.2f} "
            f"heading={math.degrees(current_heading):.1f}deg "
            f"angle_diff={math.degrees(angle_diff):.1f}deg "
            f"turn_mode={turn_mode} "
            f"shield={shield_mode} "
            f"v={linear_velocity:.2f} "
            f"w={angular_velocity:.2f}"
        )

    front_left_motor.setVelocity(left_velocity)
    back_left_motor.setVelocity(left_velocity)
    front_right_motor.setVelocity(right_velocity)
    back_right_motor.setVelocity(right_velocity)