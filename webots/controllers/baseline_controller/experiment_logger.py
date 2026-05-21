import csv
import math
from pathlib import Path
from datetime import datetime


class ExperimentLogger:
    def __init__(
        self,
        robot_name,
        level_name,
        log_root=None,
        trajectory_interval=1.0,
        summary_interval=60.0,
        near_miss_gap=1.5,
        collision_risk_gap=1.0,
    ):
        self.robot_name = robot_name
        self.level_name = level_name

        if log_root is None:
            log_root = Path(__file__).resolve().parents[3] / "data" / "logs"

        self.log_root = Path(log_root)
        self.log_root.mkdir(parents=True, exist_ok=True)

        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.trajectory_interval = trajectory_interval
        self.summary_interval = summary_interval
        self.near_miss_gap = near_miss_gap
        self.collision_risk_gap = collision_risk_gap

        self.last_trajectory_time = 0.0
        self.last_summary_time = 0.0

        self.last_x = None
        self.last_y = None

        self.distance_travelled_m = 0.0
        self.completed_tasks = 0
        self.path_planning_failures = 0

        self.traffic_wait_time_s = 0.0
        self.shield_wait_time_s = 0.0
        self.dwell_time_s = 0.0

        self.aisle_block_events = 0
        self.merge_yield_events = 0
        self.home_block_events = 0
        self.shield_interventions = 0

        self.near_miss_count = 0
        self.collision_risk_count = 0
        self.min_gap_m = float("inf")

        self.in_near_miss = False
        self.in_collision_risk = False

        self.trajectory_file = open(
            self.log_root / f"{self.run_id}_{self.level_name}_{self.robot_name}_trajectory.csv",
            "w",
            newline="",
        )
        self.event_file = open(
            self.log_root / f"{self.run_id}_{self.level_name}_{self.robot_name}_events.csv",
            "w",
            newline="",
        )
        self.summary_file = open(
            self.log_root / f"{self.run_id}_{self.level_name}_{self.robot_name}_summary.csv",
            "w",
            newline="",
        )

        self.trajectory_writer = csv.writer(self.trajectory_file)
        self.event_writer = csv.writer(self.event_file)
        self.summary_writer = csv.writer(self.summary_file)

        self.trajectory_writer.writerow([
            "time_s", "level", "robot_name", "mode",
            "x", "y", "target_x", "target_y",
            "distance_to_waypoint", "heading_rad", "angle_diff_rad",
            "linear_velocity", "angular_velocity",
            "turn_mode", "shield_mode"
        ])

        self.event_writer.writerow([
            "time_s", "level", "robot_name", "event_type", "details"
        ])

        self.summary_writer.writerow([
            "time_s", "level", "robot_name",
            "completed_tasks", "path_planning_failures",
            "distance_travelled_m",
            "traffic_wait_time_s", "shield_wait_time_s", "dwell_time_s",
            "aisle_block_events", "merge_yield_events", "home_block_events",
            "near_miss_count", "collision_risk_count",
            "shield_interventions", "min_gap_m",
            "throughput_tasks_per_min"
        ])

    def update_distance(self, x, y):
        if self.last_x is not None and self.last_y is not None:
            self.distance_travelled_m += math.hypot(x - self.last_x, y - self.last_y)

        self.last_x = x
        self.last_y = y

    def update_safety_gaps(self, time_s, current_x, current_y, other_positions):
        closest_gap = float("inf")

        for other_name, ox, oy in other_positions:
            gap = math.hypot(ox - current_x, oy - current_y)
            closest_gap = min(closest_gap, gap)

        if closest_gap == float("inf"):
            return

        self.min_gap_m = min(self.min_gap_m, closest_gap)

        if closest_gap < self.near_miss_gap and not self.in_near_miss:
            self.near_miss_count += 1
            self.in_near_miss = True
            self.log_event(time_s, "NEAR_MISS", f"gap={closest_gap:.3f}")

        if closest_gap >= self.near_miss_gap:
            self.in_near_miss = False

        if closest_gap < self.collision_risk_gap and not self.in_collision_risk:
            self.collision_risk_count += 1
            self.in_collision_risk = True
            self.log_event(time_s, "COLLISION_RISK", f"gap={closest_gap:.3f}")

        if closest_gap >= self.collision_risk_gap:
            self.in_collision_risk = False

    def add_traffic_wait(self, dt):
        self.traffic_wait_time_s += dt

    def add_shield_wait(self, dt):
        self.shield_wait_time_s += dt

    def add_dwell_time(self, dt):
        self.dwell_time_s += dt

    def count_task_completed(self, time_s, details=""):
        self.completed_tasks += 1
        self.log_event(time_s, "TASK_COMPLETED", details)

    def count_path_failure(self, time_s, details=""):
        self.path_planning_failures += 1
        self.log_event(time_s, "PATH_PLANNING_FAILED", details)

    def count_aisle_block(self, time_s, details=""):
        self.aisle_block_events += 1
        self.log_event(time_s, "AISLE_BLOCK", details)

    def count_merge_yield(self, time_s, details=""):
        self.merge_yield_events += 1
        self.log_event(time_s, "MERGE_YIELD", details)

    def count_home_block(self, time_s, details=""):
        self.home_block_events += 1
        self.log_event(time_s, "HOME_BLOCK", details)

    def count_shield_intervention(self, time_s, details=""):
        self.shield_interventions += 1
        self.log_event(time_s, "SHIELD_INTERVENTION", details)

    def log_event(self, time_s, event_type, details=""):
        self.event_writer.writerow([
            f"{time_s:.2f}",
            self.level_name,
            self.robot_name,
            event_type,
            details
        ])
        self.event_file.flush()

    def maybe_log_trajectory(
        self,
        time_s,
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
        shield_mode="NA",
    ):
        if time_s - self.last_trajectory_time < self.trajectory_interval:
            return

        self.trajectory_writer.writerow([
            f"{time_s:.2f}",
            self.level_name,
            self.robot_name,
            mode,
            f"{current_x:.3f}",
            f"{current_y:.3f}",
            f"{target_x:.3f}",
            f"{target_y:.3f}",
            f"{distance_to_waypoint:.3f}",
            f"{current_heading:.3f}",
            f"{angle_diff:.3f}",
            f"{linear_velocity:.3f}",
            f"{angular_velocity:.3f}",
            turn_mode,
            shield_mode,
        ])
        self.trajectory_file.flush()
        self.last_trajectory_time = time_s

    def maybe_write_summary(self, time_s):
        if time_s - self.last_summary_time < self.summary_interval:
            return

        throughput = self.completed_tasks / (time_s / 60.0) if time_s > 0 else 0.0
        min_gap = "" if self.min_gap_m == float("inf") else f"{self.min_gap_m:.3f}"

        self.summary_writer.writerow([
            f"{time_s:.2f}",
            self.level_name,
            self.robot_name,
            self.completed_tasks,
            self.path_planning_failures,
            f"{self.distance_travelled_m:.3f}",
            f"{self.traffic_wait_time_s:.3f}",
            f"{self.shield_wait_time_s:.3f}",
            f"{self.dwell_time_s:.3f}",
            self.aisle_block_events,
            self.merge_yield_events,
            self.home_block_events,
            self.near_miss_count,
            self.collision_risk_count,
            self.shield_interventions,
            min_gap,
            f"{throughput:.3f}",
        ])
        self.summary_file.flush()

        print(
            f"{self.robot_name} {self.level_name} SUMMARY "
            f"t={time_s:.0f}s | "
            f"tasks={self.completed_tasks} | "
            f"throughput={throughput:.2f}/min | "
            f"dist={self.distance_travelled_m:.1f}m | "
            f"traffic_wait={self.traffic_wait_time_s:.1f}s | "
            f"shield_wait={self.shield_wait_time_s:.1f}s | "
            f"near_miss={self.near_miss_count} | "
            f"collision_risk={self.collision_risk_count} | "
            f"shield={self.shield_interventions} | "
            f"min_gap={min_gap}"
        )

        self.last_summary_time = time_s