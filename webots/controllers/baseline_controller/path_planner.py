import math
import heapq
from waypoints import warehouse_waypoints


class PathPlanner:
    def __init__(self):
        self.nodes = {}
        self.graph = {}
        self._build_graph()

    def _add_node(self, node_id, point):
        self.nodes[node_id] = point
        if node_id not in self.graph:
            self.graph[node_id] = []

    def _add_edge(self, a, b):
        ax, ay = self.nodes[a]
        bx, by = self.nodes[b]
        cost = math.hypot(bx - ax, by - ay)
        self.graph[a].append((b, cost))
        self.graph[b].append((a, cost))

    def _add_directed_edge(self, a, b):
        ax, ay = self.nodes[a]
        bx, by = self.nodes[b]
        cost = math.hypot(bx - ax, by - ay)
        self.graph[a].append((b, cost))

    def _build_graph(self):
        # 1) Add all nodes
        for group_name, points in warehouse_waypoints.items():
            for i, point in enumerate(points):
                node_id = f"{group_name}_{i}"
                self._add_node(node_id, point)

        # 2) Connect internal points
        # aisle 1: bottom -> top (queue / return lane)
        # aisles 2-17: top -> bottom (task aisles)
        for group_name, points in warehouse_waypoints.items():
            is_main_aisle = (
                group_name.startswith("row_a_aisle_")
                and not group_name.endswith("_top_turn")
                and not group_name.endswith("_bottom_turn")
                and not group_name.endswith("_top_wait")
                and not group_name.endswith("_bottom_wait")
            )

            if is_main_aisle:
                if group_name == "row_a_aisle_1":
                    # aisle 1 queue lane: bottom to top
                    for i in range(len(points) - 1):
                        a = f"{group_name}_{i+1}"
                        b = f"{group_name}_{i}"
                        self._add_directed_edge(a, b)
                else:
                    # task aisles: top to bottom
                    for i in range(len(points) - 1):
                        a = f"{group_name}_{i}"
                        b = f"{group_name}_{i+1}"
                        self._add_directed_edge(a, b)
            else:
                for i in range(len(points) - 1):
                    a = f"{group_name}_{i}"
                    b = f"{group_name}_{i+1}"
                    self._add_edge(a, b)

        aisle_indices = self._rack_a_indices()

        # 3) Special aisle connections for aisles 2-17
        for idx in aisle_indices:
            if idx == 1:
                continue

            aisle = f"row_a_aisle_{idx}"
            top_turn = f"{aisle}_top_turn"
            bottom_turn = f"{aisle}_bottom_turn"
            top_wait = f"{aisle}_top_wait"
            bottom_wait = f"{aisle}_bottom_wait"

            aisle_points = warehouse_waypoints.get(aisle, [])
            top_points = warehouse_waypoints.get(top_turn, [])
            bottom_points = warehouse_waypoints.get(bottom_turn, [])
            top_wait_points = warehouse_waypoints.get(top_wait, [])
            bottom_wait_points = warehouse_waypoints.get(bottom_wait, [])

            # outbound: top wait -> top turn -> aisle
            if top_wait_points and top_points:
                self._add_directed_edge(f"{top_wait}_0", f"{top_turn}_0")

            if top_points and aisle_points:
                self._add_directed_edge(f"{top_turn}_0", f"{aisle}_0")

            # return: aisle -> bottom turn -> bottom wait
            if aisle_points and bottom_points:
                self._add_directed_edge(f"{aisle}_{len(aisle_points)-1}", f"{bottom_turn}_0")

            if bottom_points and bottom_wait_points:
                self._add_directed_edge(f"{bottom_turn}_0", f"{bottom_wait}_0")

        # 4) TOP CORRIDOR FLOW
        # Make BOTH top_wait and top_turn proper queue slots:
        # top_wait_i -> top_turn_i -> top_wait_(i+1)
        for idx in aisle_indices:
            if idx == 1:
                continue

            aisle = f"row_a_aisle_{idx}"
            top_wait_node = f"{aisle}_top_wait_0"
            top_turn_node = f"{aisle}_top_turn_0"

            if top_wait_node in self.nodes and top_turn_node in self.nodes:
                self._add_directed_edge(top_wait_node, top_turn_node)

        for idx in range(2, 17):
            this_top_turn = f"row_a_aisle_{idx}_top_turn_0"
            next_top_wait = f"row_a_aisle_{idx + 1}_top_wait_0"

            if this_top_turn in self.nodes and next_top_wait in self.nodes:
                self._add_directed_edge(this_top_turn, next_top_wait)

        # 5) BOTTOM CORRIDOR FLOW
        # Keep current logic:
        # bottom_wait_(i+1) -> bottom_wait_i
        for idx in range(2, 17):
            left_bottom_wait = f"row_a_aisle_{idx}_bottom_wait_0"
            right_bottom_wait = f"row_a_aisle_{idx + 1}_bottom_wait_0"

            if left_bottom_wait in self.nodes and right_bottom_wait in self.nodes:
                self._add_directed_edge(right_bottom_wait, left_bottom_wait)

        # 6) Aisle 1 special lane
        # Return from bottom corridor into aisle 1
        if "row_a_aisle_2_bottom_wait_0" in self.nodes and "row_a_aisle_1_bottom_turn_0" in self.nodes:
            self._add_directed_edge("row_a_aisle_2_bottom_wait_0", "row_a_aisle_1_bottom_turn_0")

        if "row_a_aisle_1_bottom_turn_0" in self.nodes and "row_a_aisle_1_7" in self.nodes:
            self._add_directed_edge("row_a_aisle_1_bottom_turn_0", "row_a_aisle_1_7")

        # Queue lane up aisle 1 ends at home
        if "row_a_aisle_1_0" in self.nodes and "row_a_aisle_1_top_turn_0" in self.nodes:
            self._add_directed_edge("row_a_aisle_1_0", "row_a_aisle_1_top_turn_0")

        # Outbound from home into top corridor
        if "row_a_aisle_1_top_turn_0" in self.nodes and "row_a_aisle_2_top_wait_0" in self.nodes:
            self._add_directed_edge("row_a_aisle_1_top_turn_0", "row_a_aisle_2_top_wait_0")

    def _rack_a_indices(self):
        found = []
        i = 1
        while True:
            if f"row_a_aisle_{i}" in warehouse_waypoints:
                found.append(i)
                i += 1
            else:
                break
        return found

    def _heuristic(self, a, b):
        ax, ay = self.nodes[a]
        bx, by = self.nodes[b]
        return math.hypot(bx - ax, by - ay)

    def _nearest_node(self, x, y):
        best_node = None
        best_dist = float("inf")
        for node_id, (nx, ny) in self.nodes.items():
            d = math.hypot(nx - x, ny - y)
            if d < best_dist:
                best_dist = d
                best_node = node_id
        return best_node

    def _reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return [self.nodes[node_id] for node_id in path]

    def find_path_by_node_ids(self, start_node, goal_node):
        if start_node not in self.nodes or goal_node not in self.nodes:
            return []

        open_heap = []
        heapq.heappush(open_heap, (0, start_node))

        came_from = {}
        g_score = {node: float("inf") for node in self.nodes}
        f_score = {node: float("inf") for node in self.nodes}

        g_score[start_node] = 0
        f_score[start_node] = self._heuristic(start_node, goal_node)

        open_set = {start_node}

        while open_heap:
            _, current = heapq.heappop(open_heap)
            open_set.discard(current)

            if current == goal_node:
                return self._reconstruct_path(came_from, current)

            for neighbor, cost in self.graph[current]:
                tentative_g = g_score[current] + cost
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, goal_node)

                    if neighbor not in open_set:
                        heapq.heappush(open_heap, (f_score[neighbor], neighbor))
                        open_set.add(neighbor)

        return []

    def find_path(self, start_x, start_y, goal_group, goal_index=0):
        start_node = self._nearest_node(start_x, start_y)
        goal_node = f"{goal_group}_{goal_index}"
        return self.find_path_by_node_ids(start_node, goal_node)


_path_planner = None


def get_path_planner():
    global _path_planner
    if _path_planner is None:
        _path_planner = PathPlanner()
    return _path_planner