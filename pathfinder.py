import heapq
from typing import List, Tuple, Optional

class PathFinder:
    def __init__(self):
        self.visited_cities = []
        self.explored_paths = []
    
    def a_star_with_coins(self, start_city, goal_city, max_coins: int):
        """
        A* algorithm with coin constraint
        Returns: (path, total_distance, coins_used) or (None, None, None) if no path exists
        """
        # Counter to ensure unique priorities and avoid City comparison
        counter = 0
        
        # Priority queue: (f_score, distance, coins_used, counter, current_city, path)
        pq = [(start_city.get_heuristic(), 0, 0, counter, start_city, [start_city])]
        visited = {}  # Maps (city, coins_used) to best distance found
        self.visited_cities = []
        self.explored_paths = []
        
        while pq:
            f_score, distance, coins_used, _, current_city, path = heapq.heappop(pq)
            
            # Track for visualization
            if current_city not in self.visited_cities:
                self.visited_cities.append(current_city)
            
            # State includes both city and coins used (for coin-constrained search)
            state = (current_city, coins_used)
            
            # Skip if we've found a better path to this state
            if state in visited and visited[state] <= distance:
                continue
            
            visited[state] = distance
            
            # Goal check
            if current_city == goal_city:
                return path, distance, coins_used
            
            # Explore neighbors
            for neighbor_city, edge_info in current_city.roads.items():
                edge_distance = edge_info['distance']
                edge_coins = edge_info['coins']
                
                new_coins = coins_used + edge_coins
                
                # Check coin constraint
                if new_coins <= max_coins:
                    new_distance = distance + edge_distance
                    h = neighbor_city.get_heuristic()
                    new_f = new_distance + h
                    new_path = path + [neighbor_city]
                    
                    # Track explored paths for visualization
                    self.explored_paths.append((current_city, neighbor_city))
                    
                    # Increment counter for unique priority
                    counter += 1
                    heapq.heappush(pq, (new_f, new_distance, new_coins, counter, neighbor_city, new_path))
        
        # No path found within coin constraint
        return None, None, None
    
    def get_visited_cities(self):
        """Returns list of cities visited during search"""
        return self.visited_cities
    
    def get_explored_paths(self):
        """Returns list of edges explored during search"""
        return self.explored_paths