import tkinter as tk
from tkinter import ttk, messagebox
from pathfinder import PathFinder

class PathFinderGUI:
    def __init__(self, root, graph):
        self.root = root
        self.graph = graph
        self.pathfinder = PathFinder()
        self.animation_running = False
        
        self.root.title("Coin-Constrained Path Finder")
        self.root.geometry("1200x800")
        
        self.create_widgets()
        self.draw_graph()
    
    def create_widgets(self):
        # Control Panel
        control_frame = tk.Frame(self.root, bg="#2c3e50", padx=20, pady=20)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title = tk.Label(control_frame, text="Path Finder", font=("Arial", 20, "bold"),
                        bg="#2c3e50", fg="white")
        title.pack(pady=(0, 20))
        
        # Start City
        tk.Label(control_frame, text="Start City:", font=("Arial", 12),
                bg="#2c3e50", fg="white").pack(anchor=tk.W, pady=(10, 5))
        self.start_var = tk.StringVar(value="A")
        start_combo = ttk.Combobox(control_frame, textvariable=self.start_var,
                                   values=self.graph.get_city_names(),
                                   state="readonly", width=20)
        start_combo.pack(pady=(0, 10))
        
        # Destination City
        tk.Label(control_frame, text="Destination:", font=("Arial", 12),
                bg="#2c3e50", fg="white").pack(anchor=tk.W, pady=(10, 5))
        self.dest_var = tk.StringVar(value="I")
        dest_combo = ttk.Combobox(control_frame, textvariable=self.dest_var,
                                  values=self.graph.get_city_names(),
                                  state="readonly", width=20)
        dest_combo.pack(pady=(0, 10))
        
        # Coin Budget
        tk.Label(control_frame, text="Coin Budget:", font=("Arial", 12),
                bg="#2c3e50", fg="white").pack(anchor=tk.W, pady=(10, 5))
        self.coins_var = tk.StringVar(value="20")
        coins_entry = tk.Entry(control_frame, textvariable=self.coins_var,
                              font=("Arial", 12), width=22)
        coins_entry.pack(pady=(0, 20))
        
        # Find Path Button
        find_btn = tk.Button(control_frame, text="Find Path", font=("Arial", 14, "bold"),
                            bg="#27ae60", fg="black", command=self.find_path,
                            relief=tk.FLAT, padx=20, pady=10)
        find_btn.pack(pady=10, fill=tk.X)
        
        # Reset Button
        reset_btn = tk.Button(control_frame, text="Reset", font=("Arial", 12),
                             bg="#e74c3c", fg="black", command=self.reset,
                             relief=tk.FLAT, padx=20, pady=10)
        reset_btn.pack(pady=5, fill=tk.X)
        
        # Info Display
        self.info_frame = tk.Frame(control_frame, bg="#34495e", relief=tk.GROOVE, bd=2)
        self.info_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(self.info_frame, text="Results", font=("Arial", 14, "bold"),
                bg="#34495e", fg="white").pack(pady=10)
        
        self.result_label = tk.Label(self.info_frame, text="", font=("Arial", 11),
                                     bg="#34495e", fg="white", justify=tk.LEFT)
        self.result_label.pack(padx=10, pady=10)
        
        # Canvas for visualization
        canvas_frame = tk.Frame(self.root, bg="white")
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#ecf0f1", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def draw_graph(self):
        """Draw the entire graph on canvas"""
        self.canvas.delete("all")
        
        # Draw edges
        for city_name, city in self.graph.cities.items():
            x1, y1 = self.graph.get_position(city_name)
            
            for neighbor, edge_info in city.roads.items():
                neighbor_name = neighbor.cityName
                if city_name < neighbor_name:  # Draw each edge only once
                    x2, y2 = self.graph.get_position(neighbor_name)
                    
                    # Draw line
                    self.canvas.create_line(x1+100, y1+50, x2+100, y2+50,
                                          fill="#95a5a6", width=2, tags="edge")
                    
                    # Draw edge labels
                    mx, my = (x1+x2)//2 + 100, (y1+y2)//2 + 50
                    self.canvas.create_text(mx, my-15, 
                                          text=f"Distance: {edge_info['distance']}",
                                          fill="#7f8c8d", font=("Arial", 9))
                    self.canvas.create_text(mx, my+5, 
                                          text=f"Coins: {edge_info['coins']}",
                                          fill="#e67e22", font=("Arial", 9, "bold"))
        
        # Draw cities
        for city_name in self.graph.get_city_names():
            x, y = self.graph.get_position(city_name)
            city = self.graph.get_city(city_name)
            
            # Draw city circle
            self.canvas.create_oval(x+80, y+30, x+120, y+70,
                                  fill="#3498db", outline="#2980b9",
                                  width=3, tags=f"city_{city_name}")
            
            # Draw city name
            self.canvas.create_text(x+100, y+50, text=city_name,
                                  fill="white", font=("Arial", 16, "bold"),
                                  tags=f"city_{city_name}")
            
            # Draw heuristic value below the city
            heuristic = city.get_heuristic()
            self.canvas.create_text(x+100, y+80, text=f"h={int(heuristic)}",
                                  fill="#9b59b6", font=("Arial", 10, "bold"),
                                  tags=f"heuristic_{city_name}")
    
    def find_path(self):
        """Execute pathfinding algorithm"""
        if self.animation_running:
            return
        
        try:
            start_name = self.start_var.get()
            goal_name = self.dest_var.get()
            max_coins = int(self.coins_var.get())
            
            if start_name == goal_name:
                messagebox.showwarning("Invalid Input", 
                                     "Start and destination must be different!")
                return
            
            start_city = self.graph.get_city(start_name)
            goal_city = self.graph.get_city(goal_name)
            
            self.animation_running = True
            self.draw_graph()
            
            # Run A* algorithm
            path, distance, coins_used = self.pathfinder.a_star_with_coins(
                start_city, goal_city, max_coins)
            
            if path is None:
                self.result_label.config(
                    text=f"NOT POSSIBLE\n\nInsufficient coins!\n\n"
                         f"No path from {start_name} to {goal_name}\n"
                         f"within {max_coins} coins budget.")
                messagebox.showinfo("No Path Found", 
                                  f"No path exists from {start_name} to {goal_name} "
                                  f"within {max_coins} coins!")
            else:
                self.animate_search(path, distance, coins_used)
                
            self.animation_running = False
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid coin budget!")
            self.animation_running = False
    
    def animate_search(self, final_path, distance, coins_used):
        """Animate the search process and final path"""
        # Show visited nodes
        visited = self.pathfinder.get_visited_cities()
        for i, city in enumerate(visited):
            self.root.after(i * 200, lambda c=city: self.highlight_visited(c))
        
        # Show final path
        delay = len(visited) * 200
        for i in range(len(final_path) - 1):
            self.root.after(delay + i * 300, 
                          lambda idx=i: self.highlight_path_edge(
                              final_path[idx], final_path[idx+1]))
        
        # Calculate step-by-step path details
        path_names = [city.cityName for city in final_path]
        path_details = "\nPath Breakdown:\n"
        cumulative_dist = 0
        cumulative_coins = 0
        
        for i in range(len(final_path) - 1):
            current = final_path[i]
            next_city = final_path[i+1]
            edge_info = current.roads[next_city]
            cumulative_dist += edge_info['distance']
            cumulative_coins += edge_info['coins']
            
            path_details += (f"{current.cityName}→{next_city.cityName}: "
                           f"Distance={edge_info['distance']}, Coins={edge_info['coins']} "
                           f"(Total: Distance={cumulative_dist}, Coins={cumulative_coins})\n")
        
        # Update result text with A* calculations
        start_h = final_path[0].get_heuristic()
        goal_h = final_path[-1].get_heuristic()
        
        result_text = (f"PATH FOUND! ✓\n\n"
                      f"Route: {' → '.join(path_names)}\n"
                      f"{path_details}\n"
                      f"A* Calculations:\n"
                      f"• g (actual): {distance}\n"
                      f"• h (start): {int(start_h)}\n"
                      f"• h (goal): {int(goal_h)}\n"
                      f"• Initial f: {int(start_h)}\n\n"
                      f"Final Stats:\n"
                      f"Total Distance (g): {distance}\n"
                      f"Coins Used: {coins_used}\n"
                      f"Cities Explored: {len(visited)}")
        
        self.root.after(delay + (len(final_path)-1) * 300, 
                       lambda: self.result_label.config(text=result_text))
    
    def highlight_visited(self, city):
        """Highlight a visited city during search"""
        x, y = self.graph.get_position(city.cityName)
        self.canvas.create_oval(x+85, y+35, x+115, y+65,
                              fill="#f39c12", outline="#e67e22",
                              width=2, tags="visited")
    
    def highlight_path_edge(self, city1, city2):
        """Highlight an edge in the final path"""
        x1, y1 = self.graph.get_position(city1.cityName)
        x2, y2 = self.graph.get_position(city2.cityName)
        
        # Draw path edge
        self.canvas.create_line(x1+100, y1+50, x2+100, y2+50,
                              fill="#27ae60", width=4, tags="path",
                              arrow=tk.LAST, arrowshape=(16, 20, 6))
        
        # Highlight path cities
        for city in [city1, city2]:
            x, y = self.graph.get_position(city.cityName)
            self.canvas.create_oval(x+80, y+30, x+120, y+70,
                                  fill="#27ae60", outline="#229954",
                                  width=3, tags="path_city")
            self.canvas.create_text(x+100, y+50, text=city.cityName,
                                  fill="white", font=("Arial", 16, "bold"))
    
    def reset(self):
        """Reset the visualization"""
        self.animation_running = False
        self.draw_graph()
        self.result_label.config(text="")