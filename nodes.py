class City:
    def __init__(self, cityName, heuristic):
        self.cityName = cityName
        self.heuristic = heuristic
        self.roads = {}  # dictionary for the city to be able to connect to multiple cities

    def connect(self, neighbor_city, distance, coins):
        """Connect to a neighbor city with distance and coin cost"""
        # Raise an error if the node connection already exists
        if neighbor_city in self.roads:
            raise ValueError(f"{self.cityName} already connected to {neighbor_city.cityName}.")
        if self in neighbor_city.roads:
            raise ValueError(f"{neighbor_city.cityName} already connected to {self.cityName}.")
        
        # Create the connection going both ways with distance and coins
        self.roads[neighbor_city] = {'distance': distance, 'coins': coins}
        neighbor_city.roads[self] = {'distance': distance, 'coins': coins}

    def get_heuristic(self):
        return self.heuristic
    
    def get_cost_to(self, neighbor_city):
        """Return the cost info if the connection exists, otherwise return None"""
        return self.roads.get(neighbor_city, None)

