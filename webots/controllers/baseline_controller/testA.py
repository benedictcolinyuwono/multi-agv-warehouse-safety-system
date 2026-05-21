from controller import Supervisor
import math
import random
from waypoints import warehouse_waypoints
from path_planner import get_path_planner
from experiment_logger import ExperimentLogger

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

# Minimal Level A home/staging queue control
QUEUE_OCCUPANCY_THRESHOLD = 1.0

HOME_GROUP = "row_a_aisle_1_top_turn"
HOME_INDEX = 0

GO_TO_TARGET = "GO_TO_TARGET"
RETURN_HOME = "RETURN_HOME"
DWELL = "DWELL"

EXPERIMENT_DURATION = 3600.0  # seconds

VALID_TASKS = []
for aisle_num in range(2, 18):
    for wp_idx in range(1, 7):
        VALID_TASKS.append((f"row_a_aisle_{aisle_num}", wp_idx))

AGV_DEF_NAMES = [f"AGV_{i}" for i in range(1, 21)]


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
    candidates = VALID_TASKS[:]
    if previous_task in candidates and len(candidates) > 1:
        candidates.remove(previous_task)
    return random.choice(candidates)


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
    bottom_turn_point = warehouse_waypoints["row_a_aisle_1_bottom_turn"][0]

    all_queue_points = aisle1_points + [home_point, bottom_turn_point]

    for px, py in all_queue_points:
        if math.hypot(target_x - px, target_y - py) < 0.5:
            return True

    return False


def is_bottom_queue_target(target_x, target_y):
    for aisle_num in range(1, 18):
        aisle_name = f"row_a_aisle_{aisle_num}"

        bottom_turn_key = f"{aisle_name}_bottom_turn"
        bottom_wait_key = f"{aisle_name}_bottom_wait"

        if bottom_turn_key in warehouse_waypoints:
            bx, by = warehouse_waypoints[bottom_turn_key][0]
            if math.hypot(target_x - bx, target_y - by) < 1.0:
                return True, aisle_name, "bottom_turn"

        if bottom_wait_key in warehouse_waypoints:
            wx, wy = warehouse_waypoints[bottom_wait_key][0]
            if math.hypot(target_x - wx, target_y - wy) < 1.0:
                return True, aisle_name, "bottom_wait"

    return False, None, None


robot_planner = get_path_planner()

current_waypoint_index = 0
step_count = 0
turn_mode = True

mode = RETURN_HOME
current_task = None
previous_task = None

waypoint_path = []
path_initialized = False

dwell_start_time = None
next_mode_after_dwell = None

initial_delay_checked = False
initial_delay_required = False

# Temporary initial dispatch rule.
# This is only used before the first task is assigned.
initial_dispatch_active = True

home_x, home_y = warehouse_waypoints[HOME_GROUP][HOME_INDEX]

logger = ExperimentLogger(robot_name, "LEVEL_A")

active_wait_key = None


def plan_new_path(current_x, current_y, goal_group, goal_index):
    return robot_planner.find_path(current_x, current_y, goal_group, goal_index)


def record_home_wait_event(time_s, dt, details):
    global active_wait_key

    logger.add_traffic_wait(dt)

    wait_key = f"HOME_BLOCK:{details}"
    if active_wait_key == wait_key:
        return

    active_wait_key = wait_key
    logger.count_home_block(time_s, details)


def record_initial_dispatch_wait_event(time_s, dt, details):
    global active_wait_key

    logger.add_traffic_wait(dt)

    wait_key = f"INITIAL_DISPATCH_WAIT:{details}"
    if active_wait_key == wait_key:
        return

    active_wait_key = wait_key
    logger.log_event(time_s, "INITIAL_DISPATCH_WAIT", details)


while robot.step(timestep) != -1:
    step_count += 1

    if step_count <= STARTUP_HOLD_STEPS:
        stop_motors()
        continue

    current_time = robot.getTime()
    dt = timestep / 1000.0

    gps_values = gps.getValues()
    current_x = gps_values[0]
    current_y = gps_values[1]

    compass_values = compass.getValues()
    current_heading = math.atan2(compass_values[0], compass_values[1])

    logger.update_distance(current_x, current_y)
    logger.update_safety_gaps(current_time, current_x, current_y, get_other_agv_positions())

    if current_time >= EXPERIMENT_DURATION:
        stop_motors()
        logger.log_event(current_time, "EXPERIMENT_FINISHED", f"duration={EXPERIMENT_DURATION:.1f}s")
        logger.maybe_write_summary(current_time)
        break

    if not initial_delay_checked:
        dist_to_home_at_start = math.hypot(current_x - home_x, current_y - home_y)

        if dist_to_home_at_start > HOME_DETECTION_THRESHOLD:
            initial_delay_required = True
            logger.log_event(
                current_time,
                "INITIAL_DELAY_REQUIRED",
                f"waiting={INITIAL_DELAY_NOT_AT_HOME:.1f}s"
            )
        else:
            initial_delay_required = False
            logger.log_event(current_time, "STARTED_AT_HOME", "no initial delay")

        initial_delay_checked = True

    if initial_delay_required and current_time < INITIAL_DELAY_NOT_AT_HOME:
        stop_motors()
        continue

    if mode == DWELL:
        stop_motors()
        logger.add_dwell_time(dt)

        if dwell_start_time is None:
            dwell_start_time = current_time

        if current_time - dwell_start_time >= DWELL_TIME:
            dwell_start_time = None

            if next_mode_after_dwell == RETURN_HOME:
                mode = RETURN_HOME
                logger.log_event(current_time, "DWELL_COMPLETE", "returning_home")

            elif next_mode_after_dwell == GO_TO_TARGET:
                previous_task = current_task
                current_task = pick_next_task(previous_task)

                # First real task has now started.
                # From this point, Level A no longer uses temporary bottom-corridor dispatch control.
                if initial_dispatch_active:
                    initial_dispatch_active = False
                    logger.log_event(
                        current_time,
                        "INITIAL_DISPATCH_COMPLETE",
                        "temporary bottom-corridor dispatch rule disabled"
                    )

                mode = GO_TO_TARGET
                logger.log_event(
                    current_time,
                    "NEW_TASK_ASSIGNED",
                    f"{current_task[0]}[{current_task[1]}]"
                )

            next_mode_after_dwell = None
            path_initialized = False
            waypoint_path = []
            current_waypoint_index = 0
            turn_mode = True
            active_wait_key = None

        logger.maybe_write_summary(current_time)
        continue

    if not path_initialized:
        if mode == GO_TO_TARGET:
            if current_task is None:
                stop_motors()
                logger.log_event(current_time, "NO_TASK_ASSIGNED", "")
                continue
            goal_group, goal_index = current_task
        else:
            goal_group, goal_index = HOME_GROUP, HOME_INDEX

        waypoint_path = plan_new_path(current_x, current_y, goal_group, goal_index)

        if waypoint_path:
            current_waypoint_index = 0
            turn_mode = True
            active_wait_key = None
            logger.log_event(
                current_time,
                "PATH_PLANNED",
                f"mode={mode}, goal={goal_group}[{goal_index}], points={len(waypoint_path)}"
            )
        else:
            waypoint_path = []
            logger.count_path_failure(current_time, f"{goal_group}[{goal_index}]")

        path_initialized = True

    if not waypoint_path or current_waypoint_index >= len(waypoint_path):
        stop_motors()
        logger.maybe_write_summary(current_time)
        continue

    target_x, target_y = waypoint_path[current_waypoint_index]

    dx = target_x - current_x
    dy = target_y - current_y
    distance_to_waypoint = math.sqrt(dx * dx + dy * dy)

    angle_to_waypoint = math.atan2(dy, dx)
    angle_diff = normalize_angle(angle_to_waypoint - current_heading)

    if distance_to_waypoint < WAYPOINT_THRESHOLD:
        current_waypoint_index += 1
        active_wait_key = None

        if current_waypoint_index >= len(waypoint_path):
            stop_motors()

            if mode == GO_TO_TARGET:
                reached_group, reached_index = current_task
                logger.count_task_completed(
                    current_time,
                    f"{reached_group}[{reached_index}]"
                )
                mode = DWELL
                next_mode_after_dwell = RETURN_HOME

            else:
                logger.log_event(current_time, "HOME_REACHED", "")
                mode = DWELL
                next_mode_after_dwell = GO_TO_TARGET

            logger.maybe_write_summary(current_time)
            continue

        continue

    # Level A common aisle 1/home staging queue control.
    # This remains active throughout the whole experiment.
    if is_aisle_1_queue_or_home_target(target_x, target_y):
        occupied, blocking_agv = point_is_occupied_by_other_agv(target_x, target_y)

        if occupied:
            record_home_wait_event(
                current_time,
                dt,
                f"target=({target_x:.2f},{target_y:.2f}), blocked_by={blocking_agv}"
            )
            stop_motors()
            logger.maybe_write_summary(current_time)
            continue

    # Temporary initial dispatch rule only.
    # This uses the Level B bottom-corridor waiting-point method only before the first task starts.
    # After INITIAL_DISPATCH_COMPLETE, Level A returns to pure baseline behaviour.
    if initial_dispatch_active:
        is_bottom_queue, bottom_aisle, bottom_point_type = is_bottom_queue_target(target_x, target_y)

        if is_bottom_queue:
            occupied, blocking_agv = point_is_occupied_by_other_agv(
                target_x,
                target_y,
                threshold=QUEUE_OCCUPANCY_THRESHOLD
            )

            if occupied:
                record_initial_dispatch_wait_event(
                    current_time,
                    dt,
                    f"{bottom_point_type}={bottom_aisle}, blocked_by={blocking_agv}"
                )

                stop_motors()
                logger.maybe_write_summary(current_time)
                continue

    active_wait_key = None

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

    left_velocity = (linear_velocity - 0.5 * AXLE_LENGTH * angular_velocity) / WHEEL_RADIUS
    right_velocity = (linear_velocity + 0.5 * AXLE_LENGTH * angular_velocity) / WHEEL_RADIUS

    logger.maybe_log_trajectory(
        current_time,
        mode,
        current_x,
        current_y,
        target_x,
        target_y,
        distance_to_waypoint,
        current_heading,
        angle_diff,
        linear_velocity,
        angular_velocity,
        turn_mode,
        "NA"
    )

    logger.maybe_write_summary(current_time)

    front_left_motor.setVelocity(left_velocity)
    back_left_motor.setVelocity(left_velocity)
    front_right_motor.setVelocity(right_velocity)
    back_right_motor.setVelocity(right_velocity)