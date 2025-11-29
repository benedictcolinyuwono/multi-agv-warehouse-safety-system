from controller import Robot, Supervisor
import math
import sys
import os

# Add shield module path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# Import shield modules
from shield.risk import assess_collision_risk_2d
from shield.limiter import limit_velocity, limit_angular_velocity
from shield.supervisor import supervise_commands, PASS, GUARDED, EMERGENCY

# Initialize robot
robot = Supervisor()
timestep = int(robot.getBasicTimeStep())
robot_name = robot.getName()

# Get motor devices
front_right_motor = robot.getDevice('front_right_wheel_joint')
front_left_motor = robot.getDevice('front_left_wheel_joint')
back_right_motor = robot.getDevice('back_right_wheel_joint')
back_left_motor = robot.getDevice('back_left_wheel_joint')

# Set motors to velocity control mode
front_right_motor.setPosition(float('inf'))
front_left_motor.setPosition(float('inf'))
back_right_motor.setPosition(float('inf'))
back_left_motor.setPosition(float('inf'))

# Get sensors
gps = robot.getDevice('gps')
gps.enable(timestep)

compass = robot.getDevice('compass')
compass.enable(timestep)

# Constants
BASE_SPEED = 15.0
WAYPOINT_THRESHOLD = 0.5
SAFETY_RADIUS = 1.0
MAX_ANGULAR_VELOCITY = 2.0
STEERING_GAIN = 5.0

# Waypoint goals
waypoint_goals = {
    'AGV_1': (10.0, 42.0),
    'AGV_2': (10.0, 36.0),
    'AGV_3': (10.0, -0.31),
    'AGV_4': (10.0, -40.0),
    'AGV_5': (10.0, -46.0),
    'AGV_6': (88.0, -10.0),
    'AGV_7': (13.0, -70.0),
    'AGV_8': (32.0, -70.0),
    'AGV_9': (45.0, -70.0),
    'AGV_10': (65.0, -70.0),
    'AGV_11': (83.0, -70.0),
    'AGV_12': (-80.0, 42.0),
    'AGV_13': (-85.0, -46.0),
    'AGV_14': (70.0, 36.0),
    'AGV_15': (-100.0, -57.0),
}

target_waypoint_x, target_waypoint_y = waypoint_goals[robot_name]

print(f"{robot_name} starting navigation to waypoint ({target_waypoint_x}, {target_waypoint_y})")

# Initialize velocity tracking
previous_x = gps.getValues()[0]
previous_y = gps.getValues()[1]
previous_time = 0.0

# Main control loop
while robot.step(timestep) != -1:
    # Read my own state
    gps_values = gps.getValues()
    current_x = gps_values[0]
    current_y = gps_values[1]
    
    compass_values = compass.getValues()
    compass_x = compass_values[0]
    compass_y = compass_values[1]
    current_heading = math.atan2(compass_y, compass_x)
    
    # Calculate my velocity
    current_time = robot.getTime()
    delta_time = current_time - previous_time
    
    if delta_time > 0.0:
        my_vx = (current_x - previous_x) / delta_time
        my_vy = (current_y - previous_y) / delta_time
    else:
        my_vx = 0.0
        my_vy = 0.0
    
    my_speed = math.sqrt(my_vx * my_vx + my_vy * my_vy)
    
    previous_x = current_x
    previous_y = current_y
    previous_time = current_time
    
    # Read other AGVs' positions
    other_agvs = []
    for i in range(1, 16):
        agv_name = f"AGV_{i}"
        if agv_name == robot_name:
            continue
        
        agv_node = robot.getFromDef(agv_name)
        if agv_node is not None:
            position = agv_node.getPosition()
            other_agvs.append({
                'name': agv_name,
                'x': position[0],
                'y': position[1],
                'z': position[2]
            })
    
    # Assess collision risk to all other AGVs
    worst_risk = {
        "ttc": math.inf,
        "headway": math.inf,
        "gap_m": math.inf,
        "margin_low": False,
        "violation_predicted": False,
    }
    closest_agv = None
    
    for other in other_agvs:
        risk = assess_collision_risk_2d(
            current_x, current_y, my_vx, my_vy,
            other['x'], other['y'],
            other_vx=0.0, other_vy=0.0,
            safety_radius=SAFETY_RADIUS
        )
        
        if risk["ttc"] < worst_risk["ttc"]:
            worst_risk = risk
            closest_agv = other['name']
    
    # Calculate vector to waypoint
    delta_x = target_waypoint_x - current_x
    delta_y = target_waypoint_y - current_y
    distance_to_waypoint = math.sqrt(delta_x * delta_x + delta_y * delta_y)
    
    # Check if waypoint reached
    if distance_to_waypoint < WAYPOINT_THRESHOLD:
        print(f"{robot_name} reached waypoint!")
        front_right_motor.setVelocity(0.0)
        front_left_motor.setVelocity(0.0)
        back_right_motor.setVelocity(0.0)
        back_left_motor.setVelocity(0.0)
        continue
    
    # Calculate desired heading to waypoint
    desired_heading = math.atan2(delta_y, delta_x)
    
    # Calculate heading error
    heading_error = desired_heading - current_heading
    if heading_error > math.pi:
        heading_error = heading_error - 2.0 * math.pi
    if heading_error < -math.pi:
        heading_error = heading_error + 2.0 * math.pi
    
    # Proportional control for steering
    angular_velocity_command = STEERING_GAIN * heading_error
    angular_velocity_command = limit_angular_velocity(angular_velocity_command, MAX_ANGULAR_VELOCITY)
    
    # Base linear velocity command
    linear_velocity_command = BASE_SPEED * 0.5
    
    # Apply safety shield
    state = {"v_cap": BASE_SPEED}
    commanded_velocities = (linear_velocity_command, angular_velocity_command)
    mode, (v_safe, w_safe) = supervise_commands(state, commanded_velocities, worst_risk)
    
    # Debug output
    if mode == EMERGENCY:
        print(f"{robot_name} [{mode}] STOPPING for {closest_agv}: TTC={worst_risk['ttc']:.2f}s")
    elif mode == GUARDED:
        print(f"{robot_name} [{mode}] Slowing for {closest_agv}: TTC={worst_risk['ttc']:.2f}s, v={v_safe:.2f}")
    
    # Apply safe velocities to motors
    left_velocity = v_safe - w_safe
    right_velocity = v_safe + w_safe
    
    front_left_motor.setVelocity(left_velocity)
    back_left_motor.setVelocity(left_velocity)
    front_right_motor.setVelocity(right_velocity)
    back_right_motor.setVelocity(right_velocity)