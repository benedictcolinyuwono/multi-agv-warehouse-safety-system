"""
Complete warehouse waypoint network for FG Warehouse
FULLY CORRECTED: Manual calculation of all aisle positions
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


# ROW A - Manual calculation of each aisle
# Racks from world file with (center_x, width)
row_a_y_start = 45.5
row_a_y_end = 82.5

# Aisle 1: Between Rack 1 (58.26, 4.35) and Rack 2 (49.84, 8.7)
# Rack 1 left edge: 58.26 - 2.175 = 56.085
# Rack 2 right edge: 49.84 + 4.35 = 54.19
# Center: (56.085 + 54.19) / 2 = 55.14
warehouse_waypoints['row_a_aisle_1'] = generate_waypoints(55.14, 55.14, row_a_y_start, row_a_y_end, 7)

# Aisle 2: Between Rack 2 (49.84, 8.7) and Rack 3 (39.24, 8.7)
# Rack 2 left: 49.84 - 4.35 = 45.49
# Rack 3 right: 39.24 + 4.35 = 43.59
# Center: (45.49 + 43.59) / 2 = 44.54
warehouse_waypoints['row_a_aisle_2'] = generate_waypoints(44.54, 44.54, row_a_y_start, row_a_y_end, 7)

# Aisle 3: Between Rack 3 (39.24, 8.7) and Rack 4 (28.64, 8.7)
warehouse_waypoints['row_a_aisle_3'] = generate_waypoints(33.94, 33.94, row_a_y_start, row_a_y_end, 7)

# Aisle 4: Between Rack 4 (28.64, 8.7) and Rack 5 (18.04, 8.7)
warehouse_waypoints['row_a_aisle_4'] = generate_waypoints(23.34, 23.34, row_a_y_start, row_a_y_end, 7)

# Aisle 5: Between Rack 5 (18.04, 8.7) and Rack 6 (7.44, 8.7)
warehouse_waypoints['row_a_aisle_5'] = generate_waypoints(12.74, 12.74, row_a_y_start, row_a_y_end, 7)

# Aisle 6: Between Rack 6 (7.44, 8.7) and Rack 7 (-3.16, 8.7)
warehouse_waypoints['row_a_aisle_6'] = generate_waypoints(2.14, 2.14, row_a_y_start, row_a_y_end, 7)

# Aisle 7: Between Rack 7 (-3.16, 8.7) and Rack 8 (-13.76, 8.7)
warehouse_waypoints['row_a_aisle_7'] = generate_waypoints(-8.46, -8.46, row_a_y_start, row_a_y_end, 7)

# Aisle 8: Between Rack 8 (-13.76, 8.7) and Rack 9 (-24.36, 8.7)
warehouse_waypoints['row_a_aisle_8'] = generate_waypoints(-19.06, -19.06, row_a_y_start, row_a_y_end, 7)

# Aisle 9: Between Rack 9 (-24.36, 8.7) and Rack 10 (-34.96, 8.7)
warehouse_waypoints['row_a_aisle_9'] = generate_waypoints(-29.66, -29.66, row_a_y_start, row_a_y_end, 7)

# Aisle 10: Between Rack 10 (-34.96, 8.7) and Rack 11 (-45.56, 8.7)
warehouse_waypoints['row_a_aisle_10'] = generate_waypoints(-40.26, -40.26, row_a_y_start, row_a_y_end, 7)

# Aisle 11: Between Rack 11 (-45.56, 8.7) and Rack 12 (-56.16, 8.7)
warehouse_waypoints['row_a_aisle_11'] = generate_waypoints(-50.86, -50.86, row_a_y_start, row_a_y_end, 7)

# Aisle 12: Between Rack 12 (-56.16, 8.7) and Rack 13 (-66.76, 8.7)
warehouse_waypoints['row_a_aisle_12'] = generate_waypoints(-61.46, -61.46, row_a_y_start, row_a_y_end, 7)

# Aisle 13: Between Rack 13 (-66.76, 8.7) and Rack 14 (-77.36, 8.7)
warehouse_waypoints['row_a_aisle_13'] = generate_waypoints(-72.06, -72.06, row_a_y_start, row_a_y_end, 7)

# Aisle 14: Between Rack 14 (-77.36, 8.7) and Rack 15 (-87.96, 8.7)
warehouse_waypoints['row_a_aisle_14'] = generate_waypoints(-82.66, -82.66, row_a_y_start, row_a_y_end, 7)

# Aisle 15: Between Rack 15 (-87.96, 8.7) and Rack 16 (-98.56, 8.7)
warehouse_waypoints['row_a_aisle_15'] = generate_waypoints(-93.26, -93.26, row_a_y_start, row_a_y_end, 7)

# Row A access corridors (CORRECTED - 0.5m clearance)
# Rack 16 at x=-98.56, width=8.7, left edge at -102.91
# Stay 0.5m clear: -102.91 - 0.5 = -103.41
warehouse_waypoints['row_a_west_access'] = generate_waypoints(-103.5, -103.5, row_a_y_start, row_a_y_end, 7)

# Rack 1 at x=58.26, width=4.35, right edge at 60.435
# Stay 0.5m clear: 60.435 + 0.5 = 60.935
warehouse_waypoints['row_a_east_access'] = generate_waypoints(61.0, 61.0, row_a_y_start, row_a_y_end, 7)


# ROW B - Manual calculation (CORRECTED)
# Racks from obstacles.py: Row B racks at y=17.1, length=31.7 (span 1.25 to 32.95)
row_b_y_start = 1.25
row_b_y_end = 32.95

# Aisle 1: Between Rack 1 (62.98, 4.35) and Rack 2 (54.58, 8.7)
# Rack 1 left: 62.98 - 2.175 = 60.805
# Rack 2 right: 54.58 + 4.35 = 58.93
# Center: (60.805 + 58.93) / 2 = 59.87
warehouse_waypoints['row_b_aisle_1'] = generate_waypoints(59.87, 59.87, row_b_y_start, row_b_y_end, 6)

# Aisle 2: Between Rack 2 (54.58, 8.7) and Rack 3 (43.98, 8.7)
# Rack 2 left: 54.58 - 4.35 = 50.23
# Rack 3 right: 43.98 + 4.35 = 48.33
# Center: (50.23 + 48.33) / 2 = 49.28
warehouse_waypoints['row_b_aisle_2'] = generate_waypoints(49.28, 49.28, row_b_y_start, row_b_y_end, 6)

# Aisle 3: Between Rack 3 (43.98, 8.7) and Rack 4 (33.38, 8.7)
# Center: 38.68
warehouse_waypoints['row_b_aisle_3'] = generate_waypoints(38.68, 38.68, row_b_y_start, row_b_y_end, 6)

# Aisle 4: Between Rack 4 (33.38, 8.7) and Rack 5 (22.78, 8.7)
# Center: 28.08
warehouse_waypoints['row_b_aisle_4'] = generate_waypoints(28.08, 28.08, row_b_y_start, row_b_y_end, 6)

# Aisle 5: Between Rack 5 (22.78, 8.7) and Rack 6 (12.18, 8.7)
# Center: 17.48
warehouse_waypoints['row_b_aisle_5'] = generate_waypoints(17.48, 17.48, row_b_y_start, row_b_y_end, 6)

# Aisle 6: Between Rack 6 (12.18, 8.7) and Rack 7 (1.58, 8.7)
# Center: 6.88
warehouse_waypoints['row_b_aisle_6'] = generate_waypoints(6.88, 6.88, row_b_y_start, row_b_y_end, 6)

# Aisle 7: Between Rack 7 (1.58, 8.7) and Rack 8 (-9.02, 8.7)
# Center: -3.72
warehouse_waypoints['row_b_aisle_7'] = generate_waypoints(-3.72, -3.72, row_b_y_start, row_b_y_end, 6)

# Aisle 8: Between Rack 8 (-9.02, 8.7) and Rack 9 (-19.62, 8.7)
# Center: -14.32
warehouse_waypoints['row_b_aisle_8'] = generate_waypoints(-14.32, -14.32, row_b_y_start, row_b_y_end, 6)

# Aisle 9: Between Rack 9 (-19.62, 8.7) and Rack 10 (-30.22, 8.7)
# Center: -24.92
warehouse_waypoints['row_b_aisle_9'] = generate_waypoints(-24.92, -24.92, row_b_y_start, row_b_y_end, 6)

# Aisle 10: Between Rack 10 (-30.22, 8.7) and Rack 11 (-40.82, 8.7)
# Center: -35.52
warehouse_waypoints['row_b_aisle_10'] = generate_waypoints(-35.52, -35.52, row_b_y_start, row_b_y_end, 6)

# Aisle 11: Between Rack 11 (-40.82, 8.7) and Rack 12 (-51.42, 8.7)
# Center: -46.12
warehouse_waypoints['row_b_aisle_11'] = generate_waypoints(-46.12, -46.12, row_b_y_start, row_b_y_end, 6)

# Aisle 12: Between Rack 12 (-51.42, 8.7) and Rack 13 (-62.02, 8.7)
# Rack 12 left: -51.42 - 4.35 = -55.77
# Rack 13 right: -62.02 + 4.35 = -57.67
# Center: (-55.77 + -57.67) / 2 = -56.72
warehouse_waypoints['row_b_aisle_12'] = generate_waypoints(-56.72, -56.72, row_b_y_start, row_b_y_end, 6)

# Row B access corridors (CORRECTED - 0.5m clearance)
# Rack 13 at x=-62.02, width=8.7, left edge at -66.37
# Stay 0.5m clear: -66.37 - 0.5 = -66.87
warehouse_waypoints['row_b_west_access'] = generate_waypoints(-67.0, -67.0, row_b_y_start, row_b_y_end, 6)

# Rack 1 at x=62.98, width=4.35, right edge at 65.155
# Stay 0.5m clear: 65.155 + 0.5 = 65.655
warehouse_waypoints['row_b_east_access'] = generate_waypoints(65.5, 65.5, row_b_y_start, row_b_y_end, 6)


# MIDDLE SECTION
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

# Middle section access corridors (CORRECTED - 0.5m clearance)
# Rack 14 at x=-57.02, width=8.7, left edge at -61.37
# Stay 0.5m clear: -61.37 - 0.5 = -61.87
warehouse_waypoints['middle_west_access'] = generate_waypoints(-62.0, -62.0, middle_y_start, middle_y_end, 7)

# Rack 1 at x=80.78, width=8.7, right edge at 85.13
# Stay 0.5m clear: 85.13 + 0.5 = 85.63
warehouse_waypoints['middle_east_access'] = generate_waypoints(86.0, 86.0, middle_y_start, middle_y_end, 7)


# BOTTOM SECTION (CORRECTED)
# Racks from obstacles.py: Bottom racks at y=-66.7, length=31.7 (span -82.55 to -50.85)
bottom_y_start = -82.55
bottom_y_end = -50.85

# Aisle 1: Between Rack 1 (-81.4, 8.7) and Rack 2 (-70.8, 8.7)
# Rack 1 right: -81.4 + 4.35 = -77.05
# Rack 2 left: -70.8 - 4.35 = -75.15
# Center: (-77.05 + -75.15) / 2 = -76.10
warehouse_waypoints['bottom_aisle_1'] = generate_waypoints(-76.10, -76.10, bottom_y_start, bottom_y_end, 6)

# Aisle 2: Between Rack 2 (-70.8, 8.7) and Rack 3 (-60.2, 8.7)
# Center: -65.5
warehouse_waypoints['bottom_aisle_2'] = generate_waypoints(-65.5, -65.5, bottom_y_start, bottom_y_end, 6)

# Aisle 3: Between Rack 3 (-60.2, 8.7) and Rack 4 (-49.6, 8.7)
# Center: -54.9
warehouse_waypoints['bottom_aisle_3'] = generate_waypoints(-54.9, -54.9, bottom_y_start, bottom_y_end, 6)

# Aisle 4: Between Rack 4 (-49.6, 8.7) and Rack 5 (-39.0, 8.7)
# Center: -44.3
warehouse_waypoints['bottom_aisle_4'] = generate_waypoints(-44.3, -44.3, bottom_y_start, bottom_y_end, 6)

# Aisle 5: Between Rack 5 (-39.0, 8.7) and Rack 6 (-28.4, 8.7)
# Center: -33.7
warehouse_waypoints['bottom_aisle_5'] = generate_waypoints(-33.7, -33.7, bottom_y_start, bottom_y_end, 6)

# Aisle 6: Between Rack 6 (-28.4, 8.7) and Rack 7 (-17.8, 8.7)
# Center: -23.1
warehouse_waypoints['bottom_aisle_6'] = generate_waypoints(-23.1, -23.1, bottom_y_start, bottom_y_end, 6)

# Aisle 7: Between Rack 7 (-17.8, 8.7) and Rack 8 (-7.2, 8.7)
# Rack 7 right: -17.8 + 4.35 = -13.45
# Rack 8 left: -7.2 - 4.35 = -11.55
# Center: (-13.45 + -11.55) / 2 = -12.5
warehouse_waypoints['bottom_aisle_7'] = generate_waypoints(-12.5, -12.5, bottom_y_start, bottom_y_end, 6)

# Bottom section access corridors (CORRECTED - 0.5m clearance)
# Rack 1 at x=-81.4, width=8.7, left edge at -85.75
# Stay 0.5m clear: -85.75 - 0.5 = -86.25
warehouse_waypoints['bottom_west_access'] = generate_waypoints(-86.5, -86.5, bottom_y_start, bottom_y_end, 6)

# Rack 8 at x=-7.2, width=8.7, right edge at -2.85
# Stay 0.5m clear: -2.85 + 0.5 = -2.35
warehouse_waypoints['bottom_east_access'] = generate_waypoints(-2.0, -2.0, bottom_y_start, bottom_y_end, 6)


# RACK R ACCESS (CORRECTED - 0.5m clearance)
# Top Rack R: center=(-95.7, 12.63), width=11.3, length=15.3
# Rack spans: x: -101.35 to -90.05, y: 4.98 to 20.28
# West access: 0.5m west of rack: -101.35 - 0.5 = -101.85
# East access: 0.5m east of rack: -90.05 + 0.5 = -89.55
warehouse_waypoints['top_rackr_west_access'] = generate_waypoints(-102.0, -102.0, 5.0, 20.0, 3)
warehouse_waypoints['top_rackr_east_access'] = generate_waypoints(-89.5, -89.5, 5.0, 20.0, 3)

# Middle Rack R: center=(83.18, -51.2), width=11.3, length=15.3
# Rack spans: x: 77.53 to 88.83, y: -58.85 to -43.55
# West access: 0.5m west of rack: 77.53 - 0.5 = 77.03
# East access: 0.5m east of rack: 88.83 + 0.5 = 89.33
warehouse_waypoints['middle_rackr_west_access'] = generate_waypoints(77.0, 77.0, -59.0, -44.0, 3)
warehouse_waypoints['middle_rackr_east_access'] = generate_waypoints(89.5, 89.5, -59.0, -44.0, 3)

# Bottom Rack R: center=(-97.75, -71.7), width=11.3, length=15.3
# Rack spans: x: -103.4 to -92.1, y: -79.35 to -64.05
# West access: 0.5m west of rack: -103.4 - 0.5 = -103.9
# East access: 0.5m east of rack: -92.1 + 0.5 = -91.6
warehouse_waypoints['bottom_rackr_west_access'] = generate_waypoints(-104.0, -104.0, -79.0, -64.0, 3)
warehouse_waypoints['bottom_rackr_east_access'] = generate_waypoints(-91.5, -91.5, -79.0, -64.0, 3)


# CONVEYOR PICKUP (CORRECTED - 2m clearance from conveyors)
# Conveyor 1A: center_x=23.02, width=30.1 (spans 7.97 to 38.07), center_y=-81.28
# Conveyor 1B: center_x=9.06, width=2.17 (spans 7.98 to 10.14), center_y=-83.48
# Conveyors span y: -81.1 to -83.48, stay 2m north: -81.1 - 2.0 = -83.1, use -79.0
# X-range: 8.0 to 38.0 (along conveyor 1A + 1B)
warehouse_waypoints['conveyor_1a_pickup'] = generate_waypoints(8.0, 38.0, -79.0, -79.0, 15)

# Conveyor 2A: center_x=55.75, width=32.19 (spans 39.66 to 71.85), center_y=-81.1
# Conveyor 2B: center_x=70.76, width=2.17 (spans 69.68 to 71.85), center_y=-83.39
# X-range: 40.0 to 72.0
warehouse_waypoints['conveyor_2a_pickup'] = generate_waypoints(40.0, 72.0, -79.0, -79.0, 16)

# Conveyor 3: center_x=90.37, width=32.1 (spans 74.32 to 106.42), center_y=-81.1
# X-range: 74.5 to 106.0
warehouse_waypoints['conveyor_3_pickup'] = generate_waypoints(74.5, 106.0, -79.0, -79.0, 16)


# CROSS-AISLES (CORRECTED - 0.5m from yellow racks, 2m from walls)
# Row A racks span y: 45.5 to 82.5
# Stay 0.5m north of racks: 82.5 + 0.5 = 83.0
# North wall at y=84.55, stay 2m south: 84.55 - 2.0 = 82.55, so use y=83.0
warehouse_waypoints['top_north_perimeter'] = generate_waypoints(-103.5, 61.0, 83.0, 83.0, 15)

# Row A south cross-aisle: 0.5m south of racks at 45.5 - 0.5 = 45.0
warehouse_waypoints['top_cross_main'] = generate_waypoints(-103.5, 61.0, 45.0, 45.0, 20)

# Row B racks span y: 1.25 to 32.95
# Stay 0.5m south: 1.25 - 0.5 = 0.75
warehouse_waypoints['row_b_south_perimeter'] = generate_waypoints(-67.0, 65.5, 0.75, 0.75, 15)

# Transition between Row B and Middle section
warehouse_waypoints['top_middle_transition'] = generate_waypoints(-67.0, 86.0, 0.75, 0.75, 18)

# Middle section racks span y: -38.65 to -1.65
# Stay 0.5m north: -1.65 + 0.5 = -1.15
warehouse_waypoints['middle_north_perimeter'] = generate_waypoints(-62.0, 86.0, -1.0, -1.0, 18)

# Middle section south: -38.65 - 0.5 = -39.15
warehouse_waypoints['middle_south_perimeter'] = generate_waypoints(-62.0, 86.0, -39.0, -39.0, 18)

# Transition between Middle and Bottom section
# Middle RackR_1 at (83.18, -51.2), width=11.3 spans x: 77.53 to 88.83
# Stay 0.5m clear of rack: 88.83 + 0.5 = 89.33, use 89.5
warehouse_waypoints['middle_bottom_transition'] = generate_waypoints(-103.5, 77.0, -44.0, -44.0, 20)

# Bottom section racks span y: -82.55 to -50.85
# Stay 0.5m north: -50.85 + 0.5 = -50.35
warehouse_waypoints['bottom_north_perimeter'] = generate_waypoints(-86.5, -2.0, -50.0, -50.0, 12)

# Bottom section south: racks at y=-66.7, length=31.7, south edge at -82.55
# Stay 0.5m clear: -82.55 - 0.5 = -83.05
warehouse_waypoints['bottom_south_perimeter'] = generate_waypoints(-86.5, -2.0, -83.0, -83.0, 12)

# Palletizing access corridor (between bottom racks and conveyors)
# 2m north of conveyors: -79.0 - 2.0 = -81.0, but racks end at -82.55
# Use midpoint: (-82.55 + -79.0) / 2 ≈ -80.75, round to -75.0 for clearance
warehouse_waypoints['palletizing_access_corridor'] = generate_waypoints(-2.0, 106.0, -75.0, -75.0, 15)

# PERIMETER CORRIDORS (CORRECTED - 0.5m from racks, 2m from walls)
# East perimeter: Row A at y=45.5-82.5, Row B at y=1.25-32.95
# Row A Rack 1 right edge: 58.26 + 2.175 = 60.435, stay 0.5m clear: 61.0
# Row B Rack 1 at x=62.98, width=4.35, spans 60.805 to 65.155
# For Row B range (y=1.25 to 32.95), need x < 60.805, use 60.5
# East wall at x=65.95, stay 2m west: 65.95 - 2.0 = 63.95
warehouse_waypoints['east_perimeter_corridor'] = [
    (61.0, 83.0), (61.0, 70.0), (61.0, 50.0), (60.5, 30.0), (60.5, 10.0),
    (65.5, -1.0), (86.0, -1.0), (86.0, -10.0), (86.0, -25.0), (86.0, -39.0),
    (0.0, -50.0), (0.0, -60.0), (0.0, -75.0)
]

# West perimeter: stay 0.5m west of Row A Rack 16 (left edge: -102.91 - 0.5 = -103.5)
# West wall at x=-106.35/42, stay 2m east: -106.35 + 2.0 = -104.35
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