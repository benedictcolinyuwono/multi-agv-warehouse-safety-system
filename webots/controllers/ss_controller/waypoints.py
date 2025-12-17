import math

warehouse_waypoints = {}

def generate_waypoints(x_start, x_end, y_start, y_end, num_points):
    waypoints = []
    if num_points == 1:
        waypoints.append(((x_start + x_end) / 2, (y_start + y_end) / 2))
    else:
        for i in range(num_points):
            t = i / (num_points - 1)
            x = x_start + t * (x_end - x_start)
            y = y_start + t * (y_end - y_start)
            waypoints.append((x, y))
    return waypoints

row_a_y_start = 45.5
row_a_y_end = 82.5

warehouse_waypoints['row_a_aisle_1'] = generate_waypoints(55.14, 55.14, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_2'] = generate_waypoints(44.54, 44.54, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_3'] = generate_waypoints(33.94, 33.94, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_4'] = generate_waypoints(23.34, 23.34, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_5'] = generate_waypoints(12.74, 12.74, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_6'] = generate_waypoints(2.14, 2.14, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_7'] = generate_waypoints(-8.46, -8.46, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_8'] = generate_waypoints(-19.06, -19.06, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_9'] = generate_waypoints(-29.66, -29.66, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_10'] = generate_waypoints(-40.26, -40.26, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_11'] = generate_waypoints(-50.86, -50.86, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_12'] = generate_waypoints(-61.46, -61.46, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_13'] = generate_waypoints(-72.06, -72.06, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_14'] = generate_waypoints(-82.66, -82.66, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_aisle_15'] = generate_waypoints(-93.26, -93.26, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_west_access'] = generate_waypoints(-103.5, -103.5, row_a_y_start, row_a_y_end, 7)
warehouse_waypoints['row_a_east_access'] = generate_waypoints(61.0, 61.0, row_a_y_start, row_a_y_end, 7)

row_b_y_start = 1.25
row_b_y_end = 32.95
warehouse_waypoints['row_b_aisle_1'] = generate_waypoints(59.87, 59.87, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_aisle_2'] = generate_waypoints(49.28, 49.28, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_aisle_3'] = generate_waypoints(38.68, 38.68, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_aisle_4'] = generate_waypoints(28.08, 28.08, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_aisle_5'] = generate_waypoints(17.48, 17.48, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_aisle_6'] = generate_waypoints(6.88, 6.88, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_aisle_7'] = generate_waypoints(-3.72, -3.72, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_aisle_8'] = generate_waypoints(-14.32, -14.32, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_aisle_9'] = generate_waypoints(-24.92, -24.92, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_aisle_10'] = generate_waypoints(-35.52, -35.52, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_aisle_11'] = generate_waypoints(-46.12, -46.12, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_aisle_12'] = generate_waypoints(-56.72, -56.72, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_west_access'] = generate_waypoints(-67.0, -67.0, row_b_y_start, row_b_y_end, 6)
warehouse_waypoints['row_b_east_access'] = generate_waypoints(65.5, 65.5, row_b_y_start, row_b_y_end, 6)

middle_y_start = -38.65
middle_y_end = -1.65

warehouse_waypoints['middle_aisle_1'] = generate_waypoints(75.48, 75.48, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_2'] = generate_waypoints(64.88, 64.88, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_3'] = generate_waypoints(54.28, 54.28, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_4'] = generate_waypoints(43.68, 43.68, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_5'] = generate_waypoints(33.08, 33.08, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_6'] = generate_waypoints(22.48, 22.48, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_7'] = generate_waypoints(11.88, 11.88, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_8'] = generate_waypoints(1.28, 1.28, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_9'] = generate_waypoints(-9.32, -9.32, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_10'] = generate_waypoints(-19.92, -19.92, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_11'] = generate_waypoints(-30.52, -30.52, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_12'] = generate_waypoints(-41.12, -41.12, middle_y_start, middle_y_end, 7)
warehouse_waypoints['middle_aisle_13'] = generate_waypoints(-51.72, -51.72, middle_y_start, middle_y_end, 7)

warehouse_waypoints['middle_west_access'] = generate_waypoints(-62.0, -62.0, middle_y_start, middle_y_end, 7)

warehouse_waypoints['middle_east_access'] = generate_waypoints(86.0, 86.0, middle_y_start, middle_y_end, 7)

bottom_y_start = -82.55
bottom_y_end = -50.85

warehouse_waypoints['bottom_aisle_1'] = generate_waypoints(-76.10, -76.10, bottom_y_start, bottom_y_end, 6)
warehouse_waypoints['bottom_aisle_2'] = generate_waypoints(-65.5, -65.5, bottom_y_start, bottom_y_end, 6)
warehouse_waypoints['bottom_aisle_3'] = generate_waypoints(-54.9, -54.9, bottom_y_start, bottom_y_end, 6)
warehouse_waypoints['bottom_aisle_4'] = generate_waypoints(-44.3, -44.3, bottom_y_start, bottom_y_end, 6)
warehouse_waypoints['bottom_aisle_5'] = generate_waypoints(-33.7, -33.7, bottom_y_start, bottom_y_end, 6)
warehouse_waypoints['bottom_aisle_6'] = generate_waypoints(-23.1, -23.1, bottom_y_start, bottom_y_end, 6)
warehouse_waypoints['bottom_aisle_7'] = generate_waypoints(-12.5, -12.5, bottom_y_start, bottom_y_end, 6)
warehouse_waypoints['bottom_west_access'] = generate_waypoints(-86.5, -86.5, bottom_y_start, bottom_y_end, 6)
warehouse_waypoints['bottom_east_access'] = generate_waypoints(-2.0, -2.0, bottom_y_start, bottom_y_end, 6)

warehouse_waypoints['top_rackr_west_access'] = generate_waypoints(-102.0, -102.0, 5.0, 20.0, 3)
warehouse_waypoints['top_rackr_east_access'] = generate_waypoints(-89.5, -89.5, 5.0, 20.0, 3)

warehouse_waypoints['middle_rackr_west_access'] = generate_waypoints(77.0, 77.0, -59.0, -44.0, 3)
warehouse_waypoints['middle_rackr_east_access'] = generate_waypoints(89.5, 89.5, -59.0, -44.0, 3)

warehouse_waypoints['bottom_rackr_west_access'] = generate_waypoints(-104.0, -104.0, -79.0, -64.0, 3)
warehouse_waypoints['bottom_rackr_east_access'] = generate_waypoints(-91.5, -91.5, -79.0, -64.0, 3)

warehouse_waypoints['conveyor_1a_pickup'] = generate_waypoints(8.0, 38.0, -79.0, -79.0, 15)
warehouse_waypoints['conveyor_2a_pickup'] = generate_waypoints(40.0, 72.0, -79.0, -79.0, 16)
warehouse_waypoints['conveyor_3_pickup'] = generate_waypoints(74.5, 106.0, -79.0, -79.0, 16)

warehouse_waypoints['top_north_perimeter'] = generate_waypoints(-103.5, 61.0, 83.0, 83.0, 15)
warehouse_waypoints['top_cross_main'] = generate_waypoints(-103.5, 61.0, 45.0, 45.0, 20)
warehouse_waypoints['row_b_south_perimeter'] = generate_waypoints(-67.0, 65.5, 0.75, 0.75, 15)
warehouse_waypoints['top_middle_transition'] = generate_waypoints(-67.0, 86.0, 0.75, 0.75, 18)

warehouse_waypoints['middle_north_perimeter'] = generate_waypoints(-62.0, 86.0, -1.0, -1.0, 18)
warehouse_waypoints['middle_south_perimeter'] = generate_waypoints(-62.0, 86.0, -39.0, -39.0, 18)
warehouse_waypoints['middle_bottom_transition'] = generate_waypoints(-103.5, 77.0, -44.0, -44.0, 20)

warehouse_waypoints['bottom_north_perimeter'] = generate_waypoints(-86.5, -2.0, -50.0, -50.0, 12)
warehouse_waypoints['bottom_south_perimeter'] = generate_waypoints(-86.5, -2.0, -83.0, -83.0, 12)

warehouse_waypoints['palletizing_access_corridor'] = generate_waypoints(-2.0, 106.0, -75.0, -75.0, 15)

warehouse_waypoints['east_perimeter_corridor'] = [
    (61.0, 83.0), (61.0, 70.0), (61.0, 50.0), (60.5, 30.0), (60.5, 10.0),
    (65.5, -1.0), (86.0, -1.0), (86.0, -10.0), (86.0, -25.0), (86.0, -39.0),
    (0.0, -50.0), (0.0, -60.0), (0.0, -75.0)
]

warehouse_waypoints['west_perimeter_corridor'] = [
    (-103.5, 83.0), (-103.5, 70.0), (-103.5, 50.0), (-103.5, 30.0), (-103.5, 10.0),
    (-103.5, 0.75), (-67.0, 0.75), (-62.0, -1.0), (-62.0, -10.0), (-62.0, -25.0), (-62.0, -39.0),
    (-86.5, -50.0), (-86.5, -60.0), (-86.5, -75.0)
]

print("=" * 70)
print("WAREHOUSE WAYPOINT NETWORK (MANUALLY CORRECTED)")
print("=" * 70)
print(f"Total Groups: {len(warehouse_waypoints)}")
total_waypoints = sum(len(wp) for wp in warehouse_waypoints.values())
print(f"Total Waypoints: {total_waypoints}")
print("=" * 70)