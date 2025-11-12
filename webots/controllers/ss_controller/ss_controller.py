from controller import Robot
import csv, os

# write logs into your repo no matter where Webots launched
HERE = os.path.dirname(__file__)
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LOGDIR = os.path.join(REPO, "data", "logs")
os.makedirs(LOGDIR, exist_ok=True)
LOGPATH = os.path.join(LOGDIR, "webots_stub.csv")

def main():
    robot = Robot()
    dt = int(robot.getBasicTimeStep())
    name = robot.getName()

    lw = robot.getDevice("left wheel")
    rw = robot.getDevice("right wheel")
    lw.setPosition(float('inf')); rw.setPosition(float('inf'))  # velocity mode
    lw.setVelocity(0.0); rw.setVelocity(0.0)

    first = not os.path.exists(LOGPATH)
    with open(LOGPATH, "a", newline="") as f:
        w = csv.writer(f)
        if first:
            w.writerow(["time_s","robot_id","v_l","v_r","note"])
        t = 0.0
        while robot.step(dt) != -1:
            v = 4.0  # rad/s
            lw.setVelocity(v); rw.setVelocity(v)
            w.writerow([t, name, v, v, "stub_running"])
            t += dt/1000.0

if __name__ == "__main__":
    main()