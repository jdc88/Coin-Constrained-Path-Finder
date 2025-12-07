from nodes import City

class CityGraph:
    def __init__(self):
        self.cities = {}  # Maps city name to City object
        self.positions = {}  # Maps city name to (x, y) for visualization
    
    def add_city(self, name: str, heuristic: float, x: int, y: int):
        """Add a city to the graph"""
        city = City(name, heuristic)
        self.cities[name] = city
        self.positions[name] = (x, y)
        return city
    
    def connect_cities(self, city1_name: str, city2_name: str, distance: int, coins: int):
        """Connect two cities with distance and coin cost"""
        city1 = self.cities[city1_name]
        city2 = self.cities[city2_name]
        
        # Modified connect method to handle distance and coins
        if city2 in city1.roads:
            raise ValueError(f"{city1_name} already connected to {city2_name}.")
        if city1 in city2.roads:
            raise ValueError(f"{city2_name} already connected to {city1_name}.")
        
        # Store both distance and coin cost
        city1.roads[city2] = {'distance': distance, 'coins': coins}
        city2.roads[city1] = {'distance': distance, 'coins': coins}
    
    def get_city(self, name: str):
        """Get a city by name"""
        return self.cities.get(name)
    
    def get_city_names(self):
        """Get list of all city names"""
        return list(self.cities.keys())
    
    def get_position(self, city_name: str):
        """Get the (x, y) position of a city"""
        return self.positions.get(city_name)


def create_sample_graph():
    """Create a sample graph for testing"""
    graph = CityGraph()
    
    # Add cities with heuristic values (straight-line distance to goal 'I')
    # Heuristics are approximate distances to city I at position (500, 500)
    cities_data = {
        "A": (1, 100, 100),     # heuristic, x, y (565, 100, 100)
        "B": (2, 300, 100),
        "C": (3, 500, 100),
        "D": (4, 100, 300),
        "E": (5, 300, 300),
        "F": (6, 500, 300),
        "G": (7, 100, 500),
        "H": (8, 300, 500),
        "I": (9, 500, 500)      
    }
    
    for name, (h, x, y) in cities_data.items():
        graph.add_city(name, h, x, y)
    
    # Add edges (city1, city2, distance, coin_cost)
    edges = [
        ("A", "B", 200, 5),
        ("B", "C", 200, 8),
        ("A", "D", 200, 3),
        ("B", "E", 200, 4),
        ("C", "F", 200, 6),
        ("D", "E", 200, 7),
        ("E", "F", 200, 5),
        ("D", "G", 200, 4),
        ("E", "H", 200, 3),
        ("F", "I", 200, 5),
        ("G", "H", 200, 6),
        ("H", "I", 200, 7),
        ("A", "E", 280, 10),  # Diagonal shortcut
        ("C", "E", 280, 9),   # Diagonal shortcut
        ("E", "G", 280, 8),   # Diagonal shortcut
        ("E", "I", 280, 11)   # Diagonal shortcut
    ]
    
    for city1, city2, dist, coins in edges:
        graph.connect_cities(city1, city2, dist, coins)
    
    return graph