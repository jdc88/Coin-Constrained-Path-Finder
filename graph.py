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
    """
    Create a sample graph with logical cost relationship:
    - Shorter paths = fewer coins
    - Longer paths = more coins
    - Creates interesting trade-offs for pathfinding
    """
    graph = CityGraph()
    
    # Add cities with heuristic values (straight-line distance to goal 'I')
    cities_data = {
        "A": (1, 100, 100),     # heuristic, x, y
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
    
    # Add edges with logical relationship: shorter distance = fewer coins
    # Standard edges (distance=200, coins proportional)
    edges = [
        # Horizontal edges (distance 200)
        ("A", "B", 200, 2),   # 4 coins per 200 units
        ("B", "C", 200, 2),
        ("D", "E", 200, 2),
        ("E", "F", 200, 2),
        ("G", "H", 200, 2),
        ("H", "I", 200, 2),
        
        # Vertical edges (distance 200)
        ("A", "D", 200, 2),
        ("B", "E", 200, 2),
        ("C", "F", 200, 2),
        ("D", "G", 200, 2),
        ("E", "H", 200, 2),
        ("F", "I", 200, 2),
        
        # Diagonal shortcuts (distance 280, MORE coins due to longer distance)
        ("A", "E", 280, 4),
        ("C", "E", 280, 4),
        ("E", "G", 280, 4),
        ("E", "I", 280, 4)
    ]
    
    for city1, city2, dist, coins in edges:
        graph.connect_cities(city1, city2, dist, coins)
    
    return graph


def create_interesting_graph():
    """
    Create a graph with interesting trade-offs:
    - Some cheap but long paths
    - Some expensive but short paths
    - Forces strategic thinking about coin budget
    """
    graph = CityGraph()
    
    # Add cities with heuristic values
    cities_data = {
        "A": (1, 100, 100),
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
    
    # Create interesting trade-offs
    edges = [
        # Standard roads (distance 200, moderate cost)
        ("A", "B", 200, 5),
        ("B", "C", 200, 5),
        ("D", "E", 200, 5),
        ("E", "F", 200, 5),
        ("G", "H", 200, 5),
        ("H", "I", 200, 5),
        
        # Cheap vertical roads (good for budget-conscious paths)
        ("A", "D", 200, 3),
        ("B", "E", 200, 3),
        ("C", "F", 200, 3),
        ("D", "G", 200, 3),
        ("E", "H", 200, 3),
        ("F", "I", 200, 3),
        
        # Expensive diagonal shortcuts (fast but costly)
        ("A", "E", 280, 9),   # Expensive shortcut
        ("C", "E", 280, 9),   # Expensive shortcut
        ("E", "G", 280, 9),   # Expensive shortcut
        ("E", "I", 280, 9)    # Expensive shortcut
    ]
    
    for city1, city2, dist, coins in edges:
        graph.connect_cities(city1, city2, dist, coins)
    
    return graph