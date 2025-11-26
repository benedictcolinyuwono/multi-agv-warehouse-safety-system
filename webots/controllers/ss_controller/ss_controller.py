from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())
name = robot.getName()

fr = robot.getDevice('front_right_wheel_joint')
fl = robot.getDevice('front_left_wheel_joint')
br = robot.getDevice('back_right_wheel_joint')
bl = robot.getDevice('back_left_wheel_joint')

motors = [fr, fl, br, bl]

for m in motors:
    m.setPosition(float('inf'))

BASE_SPEED = 15.0

while robot.step(timestep) != -1:
    for m in motors:
        m.setVelocity(BASE_SPEED)