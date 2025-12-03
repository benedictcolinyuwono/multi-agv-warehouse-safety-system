"""
A* Path Planning for Warehouse Navigation
Builds waypoint connectivity graph and finds optimal paths
"""

import math
from waypoints import warehouse_waypoints

class PathPlanner:
    def __init__(self, max_connection_distance=25.0):
        """
        Initialize path planner with waypoint network
        
        Args:
            max_connection_distance: Maximum distance to connect waypoints (meters)
        """
        self.waypoints = warehouse_waypoints
        self.graph = {}
        self.max_connection_distance = max_connection_distance
        self._build_graph()
    
    def _build_graph(self):
        """Build connectivity graph between waypoints"""
        # Flatten waypoints into single list with IDs
        self.waypoint_list = []
        self.waypoint_coords = {}
        
        waypoint_id = 0
        for aisle_name, positions in self.waypoints.items():
            for i, (x, y) in enumerate(positions):
                wp_id = f"{aisle_name}_{i}"
                self.waypoint_list.append(wp_id)
                self.waypoint_coords[wp_id] = (x, y)
                waypoint_id += 1
        
        print(f"Building graph with {len(self.waypoint_list)} waypoints...")
        
        # Build adjacency list
        for wp1_id in self.waypoint_list:
            self.graph[wp1_id] = []
            x1, y1 = self.waypoint_coords[wp1_id]
            
            for wp2_id in self.waypoint_list:
                if wp1_id == wp2_id:
                    continue
                
                x2, y2 = self.waypoint_coords[wp2_id]
                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                # Connect if within reasonable distance
                if distance <= self.max_connection_distance:
                    self.graph[wp1_id].append((wp2_id, distance))
        
        print(f"Graph built with {sum(len(neighbors) for neighbors in self.graph.values())} edges")
    
    def _heuristic(self, wp_id, goal_id):
        """A* heuristic: Euclidean distance to goal"""
        x1, y1 = self.waypoint_coords[wp_id]
        x2, y2 = self.waypoint_coords[goal_id]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def find_path(self, start_x, start_y, goal_aisle, goal_position):
        """
        Find optimal path from start position to goal waypoint using A*
        
        Args:
            start_x, start_y: Starting position
            goal_aisle: Target aisle name (e.g., 'row_a_aisle_1')
            goal_position: Position index in aisle (e.g., 3)
        
        Returns:
            List of (x, y) coordinates representing path
        """
        # Find nearest waypoint to start
        start_wp_id = self._find_nearest_waypoint(start_x, start_y)
        
        # Get goal waypoint ID
        goal_wp_id = f"{goal_aisle}_{goal_position}"
        
        if goal_wp_id not in self.waypoint_coords:
            print(f"ERROR: Goal waypoint {goal_wp_id} not found!")
            return None
        
        print(f"Pathfinding: {start_wp_id} -> {goal_wp_id}")
        
        # A* algorithm
        open_set = {start_wp_id}
        came_from = {}
        
        g_score = {wp_id: math.inf for wp_id in self.waypoint_list}
        g_score[start_wp_id] = 0
        
        f_score = {wp_id: math.inf for wp_id in self.waypoint_list}
        f_score[start_wp_id] = self._heuristic(start_wp_id, goal_wp_id)
        
        while open_set:
            # Get node with lowest f_score
            current = min(open_set, key=lambda wp: f_score[wp])
            
            if current == goal_wp_id:
                # Reconstruct path
                path = self._reconstruct_path(came_from, current)
                print(f"Path found with {len(path)} waypoints")
                return path
            
            open_set.remove(current)
            
            # Explore neighbors
            for neighbor, edge_cost in self.graph[current]:
                tentative_g = g_score[current] + edge_cost
                
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, goal_wp_id)
                    
                    if neighbor not in open_set:
                        open_set.add(neighbor)
        
        print("ERROR: No path found!")
        return None
    
    def _find_nearest_waypoint(self, x, y):
        """Find closest waypoint to given position"""
        min_dist = math.inf
        nearest = None
        
        for wp_id, (wx, wy) in self.waypoint_coords.items():
            dist = math.sqrt((wx - x)**2 + (wy - y)**2)
            if dist < min_dist:
                min_dist = dist
                nearest = wp_id
        
        return nearest
    
    def _reconstruct_path(self, came_from, current):
        """Reconstruct path from A* search"""
        path = [self.waypoint_coords[current]]
        
        while current in came_from:
            current = came_from[current]
            path.append(self.waypoint_coords[current])
        
        path.reverse()
        return path


# GLOBAL PATH PLANNER INSTANCE
path_planner = None

def get_path_planner():
    """Get or create global path planner instance"""
    global path_planner
    if path_planner is None:
        path_planner = PathPlanner(max_connection_distance=25.0)
    return path_planner


if __name__ == "__main__":
    # Test path planner
    planner = PathPlanner()
    
    # Test path from AGV_1 start to target
    test_path = planner.find_path(4.89, 41.15, 'row_a_aisle_1', 3)
    
    if test_path:
        print("\nTest path found:")
        for i, (x, y) in enumerate(test_path):
            print(f"  Waypoint {i+1}: ({x:.2f}, {y:.2f})")