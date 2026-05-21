SHIELD_SAFETY_RADIUS = 0.5
SHIELD_NEIGHBOR_RADIUS = 5.0


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

        relative_x = ox - current_x
        relative_y = oy - current_y

        motion_mag = math.hypot(ego_vx, ego_vy)

        # Ignore AGVs clearly behind the ego AGV.
        if motion_mag > 0.05:
            forward_dot = (relative_x * ego_vx + relative_y * ego_vy) / motion_mag

            if forward_dot < -0.2:
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


def record_shield_event(time_s, dt, shield_mode, blocking_agv, critical_risk):
    global active_shield_key

    if shield_mode == "PASS":
        active_shield_key = None
        return

    logger.add_shield_wait(dt)

    shield_key = f"{shield_mode}:{blocking_agv}"
    if active_shield_key == shield_key:
        return

    active_shield_key = shield_key

    logger.count_shield_intervention(
        time_s,
        f"mode={shield_mode}, blocker={blocking_agv}, "
        f"ttc={critical_risk['ttc']:.3f}, "
        f"headway={critical_risk['headway']:.3f}, "
        f"gap={critical_risk['gap_m']:.3f}"
    )


shield_mode = "PASS"

# Apply the supervisory layer only during forward movement.
if (not turn_mode) and (not is_aisle_1_queue_or_home_target(target_x, target_y)):
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

        record_shield_event(current_time, dt, shield_mode, blocking_agv, critical_risk)
    else:
        active_shield_key = None
else:
    active_shield_key = None