"""
Complete warehouse waypoint network for FG Warehouse
Total: ~600 waypoints covering pick/put aisles, perimeter access, and cross-aisles
"""

import math

warehouse_waypoints = {}

def generate_waypoints(x_start, x_end, y_start, y_end, num_points):
    """Generate evenly spaced waypoints between two points"""
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


# TOP SECTION - ROW A
row_a_rack_centers = [58.26, 49.84, 39.24, 28.64, 18.04, 7.44, -3.16, -13.76, 
                      -24.36, -34.96, -45.56, -56.16, -66.76, -77.36, -87.96, -98.56]
row_a_y_start = 45.5
row_a_y_end = 82.5

for i in range(15):
    aisle_x = (row_a_rack_centers[i] + row_a_rack_centers[i + 1]) / 2
    aisle_name = f'row_a_aisle_{i + 1}'
    warehouse_waypoints[aisle_name] = generate_waypoints(
        aisle_x, aisle_x, row_a_y_start, row_a_y_end, 7
    )

row_a_west_x = row_a_rack_centers[-1] - 8.7/2 - 1.0
warehouse_waypoints['row_a_west_access'] = generate_waypoints(
    row_a_west_x, row_a_west_x, row_a_y_start, row_a_y_end, 7
)

row_a_east_x = row_a_rack_centers[0] + 4.35/2 + 1.0
warehouse_waypoints['row_a_east_access'] = generate_waypoints(
    row_a_east_x, row_a_east_x, row_a_y_start, row_a_y_end, 7
)


# TOP SECTION - ROW B
row_b_rack_centers = [62.98, 54.58, 43.98, 33.38, 22.78, 12.18, 1.58, 
                      -9.02, -19.62, -30.22, -40.82, -51.42, -62.02]
row_b_y_start = 1.25
row_b_y_end = 32.95

for i in range(12):
    aisle_x = (row_b_rack_centers[i] + row_b_rack_centers[i + 1]) / 2
    aisle_name = f'row_b_aisle_{i + 1}'
    warehouse_waypoints[aisle_name] = generate_waypoints(
        aisle_x, aisle_x, row_b_y_start, row_b_y_end, 6
    )

row_b_west_x = row_b_rack_centers[-1] - 8.7/2 - 1.0
warehouse_waypoints['row_b_west_access'] = generate_waypoints(
    row_b_west_x, row_b_west_x, row_b_y_start, row_b_y_end, 6
)

row_b_east_x = row_b_rack_centers[0] + 4.35/2 + 1.0
warehouse_waypoints['row_b_east_access'] = generate_waypoints(
    row_b_east_x, row_b_east_x, row_b_y_start, row_b_y_end, 6
)


# MIDDLE SECTION - MIDDLE ROW
middle_rack_centers = [80.78, 70.18, 59.58, 48.98, 38.38, 27.78, 17.18, 
                       6.58, -4.02, -14.62, -25.22, -35.82, -46.42, -57.02]
middle_y_start = -38.65
middle_y_end = -1.65

for i in range(13):
    aisle_x = (middle_rack_centers[i] + middle_rack_centers[i + 1]) / 2
    aisle_name = f'middle_aisle_{i + 1}'
    warehouse_waypoints[aisle_name] = generate_waypoints(
        aisle_x, aisle_x, middle_y_start, middle_y_end, 7
    )

middle_west_x = middle_rack_centers[-1] - 8.7/2 - 1.0
warehouse_waypoints['middle_west_access'] = generate_waypoints(
    middle_west_x, middle_west_x, middle_y_start, middle_y_end, 7
)

middle_east_x = middle_rack_centers[0] + 8.7/2 + 1.0
warehouse_waypoints['middle_east_access'] = generate_waypoints(
    middle_east_x, middle_east_x, middle_y_start, middle_y_end, 7
)


# BOTTOM SECTION - BOTTOM ROW
bottom_rack_centers = [-81.4, -70.8, -60.2, -49.6, -39.0, -28.4, -17.8, -7.2]
bottom_y_start = -82.55
bottom_y_end = -50.85

for i in range(7):
    aisle_x = (bottom_rack_centers[i] + bottom_rack_centers[i + 1]) / 2
    aisle_name = f'bottom_aisle_{i + 1}'
    warehouse_waypoints[aisle_name] = generate_waypoints(
        aisle_x, aisle_x, bottom_y_start, bottom_y_end, 6
    )

bottom_west_x = bottom_rack_centers[0] - 8.7/2 - 1.0
warehouse_waypoints['bottom_west_access'] = generate_waypoints(
    bottom_west_x, bottom_west_x, bottom_y_start, bottom_y_end, 6
)

bottom_east_x = bottom_rack_centers[-1] + 8.7/2 + 1.0
warehouse_waypoints['bottom_east_access'] = generate_waypoints(
    bottom_east_x, bottom_east_x, bottom_y_start, bottom_y_end, 6
)


# RACK R ACCESS
top_rackr_y_start = 12.63 - 15.3/2
top_rackr_y_end = 12.63 + 15.3/2
top_rackr_west_x = -95.7 - 11.3/2 - 1.0
top_rackr_east_x = -95.7 + 11.3/2 + 1.0

warehouse_waypoints['top_rackr_west_access'] = generate_waypoints(
    top_rackr_west_x, top_rackr_west_x, top_rackr_y_start, top_rackr_y_end, 3
)
warehouse_waypoints['top_rackr_east_access'] = generate_waypoints(
    top_rackr_east_x, top_rackr_east_x, top_rackr_y_start, top_rackr_y_end, 3
)

middle_rackr_y_start = -51.2 - 15.3/2
middle_rackr_y_end = -51.2 + 15.3/2
middle_rackr_west_x = 83.18 - 11.3/2 - 1.0
middle_rackr_east_x = 83.18 + 11.3/2 + 1.0

warehouse_waypoints['middle_rackr_west_access'] = generate_waypoints(
    middle_rackr_west_x, middle_rackr_west_x, middle_rackr_y_start, middle_rackr_y_end, 3
)
warehouse_waypoints['middle_rackr_east_access'] = generate_waypoints(
    middle_rackr_east_x, middle_rackr_east_x, middle_rackr_y_start, middle_rackr_y_end, 3
)

bottom_rackr_y_start = -71.7 - 15.3/2
bottom_rackr_y_end = -71.7 + 15.3/2
bottom_rackr_west_x = -97.75 - 11.3/2 - 1.0
bottom_rackr_east_x = -97.75 + 11.3/2 + 1.0

warehouse_waypoints['bottom_rackr_west_access'] = generate_waypoints(
    bottom_rackr_west_x, bottom_rackr_west_x, bottom_rackr_y_start, bottom_rackr_y_end, 3
)
warehouse_waypoints['bottom_rackr_east_access'] = generate_waypoints(
    bottom_rackr_east_x, bottom_rackr_east_x, bottom_rackr_y_start, bottom_rackr_y_end, 3
)


# PALLETIZING CONVEYOR PICKUP POINTS
conv1a_north_y = -81.28 + 2.17/2 + 0.5
conv1a_x_start = 23.02 - 30.1/2
conv1a_x_end = 23.02 + 30.1/2
warehouse_waypoints['conveyor_1a_pickup'] = generate_waypoints(
    conv1a_x_start, conv1a_x_end, conv1a_north_y, conv1a_north_y, 15
)

conv2a_north_y = -81.1 + 2.17/2 + 0.5
conv2a_x_start = 55.75 - 32.19/2
conv2a_x_end = 55.75 + 32.19/2
warehouse_waypoints['conveyor_2a_pickup'] = generate_waypoints(
    conv2a_x_start, conv2a_x_end, conv2a_north_y, conv2a_north_y, 16
)

conv3_north_y = -81.1 + 2.17/2 + 0.5
conv3_x_start = 90.37 - 32.1/2
conv3_x_end = 90.37 + 32.1/2
warehouse_waypoints['conveyor_3_pickup'] = generate_waypoints(
    conv3_x_start, conv3_x_end, conv3_north_y, conv3_north_y, 16
)


# CROSS-AISLE NAVIGATION
warehouse_waypoints['top_north_perimeter'] = generate_waypoints(
    -98.0, 58.0, 83.5, 83.5, 15
)

warehouse_waypoints['top_cross_main'] = generate_waypoints(
    -98.0, 62.0, 39.0, 39.0, 20
)

warehouse_waypoints['row_b_south_perimeter'] = generate_waypoints(
    -62.0, 62.0, 0.0, 0.0, 15
)

warehouse_waypoints['top_middle_transition'] = generate_waypoints(
    -57.0, 80.0, -1.0, -1.0, 18
)

warehouse_waypoints['middle_north_perimeter'] = generate_waypoints(
    -57.0, 85.0, -2.0, -2.0, 18
)

warehouse_waypoints['middle_south_perimeter'] = generate_waypoints(
    -57.0, 85.0, -39.0, -39.0, 18
)

warehouse_waypoints['middle_bottom_transition'] = generate_waypoints(
    -98.0, 85.0, -45.0, -45.0, 20
)

warehouse_waypoints['bottom_north_perimeter'] = generate_waypoints(
    -98.0, 5.0, -51.0, -51.0, 12
)

warehouse_waypoints['bottom_south_perimeter'] = generate_waypoints(
    -98.0, 5.0, -83.0, -83.0, 12
)

warehouse_waypoints['palletizing_access_corridor'] = generate_waypoints(
    0.0, 100.0, -70.0, -70.0, 15
)

warehouse_waypoints['east_perimeter_corridor'] = [
    (63.0, 80.0), (63.0, 60.0), (63.0, 40.0), (63.0, 20.0), (63.0, 5.0),
    (88.0, -5.0), (88.0, -20.0), (88.0, -35.0), (88.0, -50.0),
    (5.0, -55.0), (5.0, -65.0), (5.0, -75.0)
]

warehouse_waypoints['west_perimeter_corridor'] = [
    (-103.0, 80.0), (-103.0, 60.0), (-103.0, 40.0), (-103.0, 20.0), (-103.0, 5.0),
    (-80.0, -5.0), (-80.0, -20.0), (-80.0, -35.0), (-80.0, -50.0),
    (-103.0, -55.0), (-103.0, -65.0), (-103.0, -75.0), (-103.0, -80.0)
]


# SUMMARY
print("=" * 70)
print("WAREHOUSE WAYPOINT NETWORK GENERATED")
print("=" * 70)
print(f"Total Aisle Groups: {len(warehouse_waypoints)}")
total_waypoints = sum(len(waypoints) for waypoints in warehouse_waypoints.values())
print(f"Total Waypoints: {total_waypoints}")
print("=" * 70)

if __name__ == "__main__":
    print("\nSample waypoints from Row A Aisle 1:")
    for i, waypoint in enumerate(warehouse_waypoints['row_a_aisle_1']):
        print(f"  Position {i+1}: {waypoint}")