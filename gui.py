# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from pathfinder import PathFinder

class PathFinderGUI:
    def __init__(self, root, graph):
        self.root = root
        self.graph = graph
        self.pathfinder = PathFinder()
        self.animation_running = False
        
        # Game state
        self.game_mode = "setup"  # setup, playing, comparing
        self.start_city = None
        self.goal_city = None
        self.current_city = None
        self.user_path = []
        self.user_distance = 0
        self.user_coins = 0
        self.max_coins = 0
        
        self.root.title("Coin-Constrained Path Finder - Interactive Game")
        self.root.geometry("1400x900")
        
        self.create_widgets()
        self.draw_graph()
    
    def create_widgets(self):
        # Control Panel
        control_frame = tk.Frame(self.root, bg="#ecf0f1", padx=15, pady=15)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title = tk.Label(control_frame, text="Path Finder Game", font=("Arial", 16, "bold"),
                        bg="#ecf0f1", fg="black")
        title.pack(pady=(0, 15))
        
        # Game Instructions
        self.instruction_label = tk.Label(control_frame, 
                                         text="Step 1: Set up your game",
                                         font=("Arial", 10, "bold"),
                                         bg="#ecf0f1", fg="#34495e", 
                                         wraplength=200, justify=tk.LEFT)
        self.instruction_label.pack(pady=(0, 12))
        
        # Start City
        tk.Label(control_frame, text="Start City:", font=("Arial", 11),
                bg="#ecf0f1", fg="black").pack(anchor=tk.W, pady=(8, 3))
        self.start_var = tk.StringVar(value="NYC")
        self.start_combo = ttk.Combobox(control_frame, textvariable=self.start_var,
                                   values=self.graph.get_city_names(),
                                   state="readonly", width=18)
        self.start_combo.pack(pady=(0, 8))
        
        # Destination City
        tk.Label(control_frame, text="Destination:", font=("Arial", 11),
                bg="#ecf0f1", fg="black").pack(anchor=tk.W, pady=(8, 3))
        self.dest_var = tk.StringVar(value="LA")
        self.dest_combo = ttk.Combobox(control_frame, textvariable=self.dest_var,
                                  values=self.graph.get_city_names(),
                                  state="readonly", width=18)
        self.dest_combo.pack(pady=(0, 8))
        
        # Coin Budget
        tk.Label(control_frame, text="Coin Budget:", font=("Arial", 11),
                bg="#ecf0f1", fg="black").pack(anchor=tk.W, pady=(8, 3))
        self.coins_var = tk.StringVar(value="25")
        self.coins_entry = tk.Entry(control_frame, textvariable=self.coins_var,
                              font=("Arial", 11), width=20)
        self.coins_entry.pack(pady=(0, 15))
        
        # Buttons Frame
        buttons_frame = tk.Frame(control_frame, bg="#ecf0f1")
        buttons_frame.pack(fill=tk.X, pady=5)
        
        # Start Game Button
        self.start_game_btn = tk.Button(buttons_frame, text="Start Game", 
                                        font=("Arial", 12, "bold"),
                                        bg="#27ae60", fg="black", 
                                        command=self.start_game,
                                        relief=tk.FLAT, padx=15, pady=8)
        self.start_game_btn.pack(pady=5, fill=tk.X)
        
        # Submit Path Button (hidden initially)
        self.submit_btn = tk.Button(buttons_frame, text="Submit My Path", 
                                    font=("Arial", 12, "bold"),
                                    bg="#9b59b6", fg="black", 
                                    command=self.submit_path,
                                    relief=tk.FLAT, padx=15, pady=8)
        
        # Undo Last Move Button (hidden initially)
        self.undo_btn = tk.Button(buttons_frame, text="Undo Last Move", 
                                  font=("Arial", 10),
                                  bg="#f39c12", fg="black", 
                                  command=self.undo_move,
                                  relief=tk.FLAT, padx=15, pady=6)
        
        # Show AI Solution Button (hidden initially)
        self.ai_solution_btn = tk.Button(buttons_frame, text="Show AI Solution", 
                                         font=("Arial", 11),
                                         bg="#3498db", fg="black", 
                                         command=self.show_ai_solution,
                                         relief=tk.FLAT, padx=15, pady=7)
        
        # Reset Button
        self.reset_btn = tk.Button(buttons_frame, text="Reset Game", 
                                   font=("Arial", 10),
                                   bg="#e74c3c", fg="black", 
                                   command=self.reset_game,
                                   relief=tk.FLAT, padx=15, pady=7)
        self.reset_btn.pack(pady=5, fill=tk.X)
        
        # Info Display
        self.info_frame = tk.Frame(control_frame, bg="white", relief=tk.GROOVE, bd=2)
        self.info_frame.pack(pady=15, fill=tk.BOTH, expand=True)
        
        tk.Label(self.info_frame, text="Game Status", font=("Arial", 12, "bold"),
                bg="white", fg="black").pack(pady=8)
        
        self.result_label = tk.Label(self.info_frame, text="Set up your game and click Start!", 
                                     font=("Arial", 10),
                                     bg="white", fg="black", justify=tk.LEFT)
        self.result_label.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
        
        # Canvas for visualization
        canvas_frame = tk.Frame(self.root, bg="white")
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#ecf0f1", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind click events
        self.canvas.bind("<Button-1>", self.on_city_click)
    
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
                                          text=f"D:{edge_info['distance']}",
                                          fill="#7f8c8d", font=("Arial", 9))
                    self.canvas.create_text(mx, my+5, 
                                          text=f"C:{edge_info['coins']}",
                                          fill="#e67e22", font=("Arial", 9, "bold"))
        
        # Draw cities
        for city_name in self.graph.get_city_names():
            x, y = self.graph.get_position(city_name)
            city = self.graph.get_city(city_name)
            
            # Determine city color based on state
            if self.game_mode == "playing":
                if city == self.current_city:
                    color = "#27ae60"  # Green for current
                    outline = "#229954"
                elif city == self.start_city:
                    color = "#3498db"  # Blue for start
                    outline = "#2980b9"
                elif city == self.goal_city:
                    color = "#e74c3c"  # Red for goal
                    outline = "#c0392b"
                elif city in [self.graph.get_city(c.cityName) for c in self.user_path]:
                    color = "#f39c12"  # Orange for visited
                    outline = "#e67e22"
                else:
                    color = "#95a5a6"  # Gray for unvisited
                    outline = "#7f8c8d"
            else:
                color = "#3498db"
                outline = "#2980b9"
            
            # Draw city circle
            self.canvas.create_oval(x+80, y+30, x+120, y+70,
                                  fill=color, outline=outline,
                                  width=3, tags=f"city_{city_name}")
            
            # Draw city name
            self.canvas.create_text(x+100, y+50, text=city_name,
                                  fill="white", font=("Arial", 12, "bold"),
                                  tags=f"city_{city_name}")
            
            # Draw heuristic value below the city
            heuristic = city.get_heuristic()
            self.canvas.create_text(x+100, y+80, text=f"h={int(heuristic)}",
                                  fill="#9b59b6", font=("Arial", 10, "bold"),
                                  tags=f"heuristic_{city_name}")
    
    def start_game(self):
        """Initialize the game"""
        try:
            start_name = self.start_var.get()
            goal_name = self.dest_var.get()
            self.max_coins = int(self.coins_var.get())
            
            if start_name == goal_name:
                messagebox.showwarning("Invalid Input", 
                                     "Start and destination must be different!")
                return
            
            self.start_city = self.graph.get_city(start_name)
            self.goal_city = self.graph.get_city(goal_name)
            self.current_city = self.start_city
            self.user_path = [self.start_city]
            self.user_distance = 0
            self.user_coins = 0
            self.game_mode = "playing"
            
            # Update UI
            self.start_combo.config(state="disabled")
            self.dest_combo.config(state="disabled")
            self.coins_entry.config(state="disabled")
            self.start_game_btn.pack_forget()
            self.submit_btn.pack(pady=5, fill=tk.X)
            self.undo_btn.pack(pady=5, fill=tk.X)
            self.ai_solution_btn.pack(pady=5, fill=tk.X)
            
            self.instruction_label.config(
                text="Click cities to build path\nClick Submit when ready!")
            
            self.update_status()
            self.draw_graph()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid coin budget!")
    
    def on_city_click(self, event):
        """Handle city click during gameplay"""
        if self.game_mode != "playing":
            return
        
        # Find which city was clicked
        clicked_city = None
        for city_name in self.graph.get_city_names():
            x, y = self.graph.get_position(city_name)
            if (x+80 <= event.x <= x+120) and (y+30 <= event.y <= y+70):
                clicked_city = self.graph.get_city(city_name)
                break
        
        if clicked_city is None:
            return
        
        # Check if this city is a valid neighbor
        if clicked_city in self.current_city.roads:
            edge_info = self.current_city.roads[clicked_city]
            new_coins = self.user_coins + edge_info['coins']
            
            # Check coin constraint
            if new_coins > self.max_coins:
                messagebox.showwarning("Insufficient Coins!", 
                                     f"This route costs {edge_info['coins']} coins.\n"
                                     f"You only have {self.max_coins - self.user_coins} coins left!")
                return
            
            # Valid move!
            self.user_path.append(clicked_city)
            self.user_distance += edge_info['distance']
            self.user_coins += edge_info['coins']
            self.current_city = clicked_city
            
            self.update_status()
            self.draw_graph()
            self.draw_user_path()
            
        elif clicked_city == self.current_city:
            return  # Already here
        else:
            messagebox.showinfo("Invalid Move", 
                              "You can only move to connected cities!\n"
                              "Check the paths from your current location.")
    
    def draw_user_path(self):
        """Draw the user's chosen path"""
        for i in range(len(self.user_path) - 1):
            city1 = self.user_path[i]
            city2 = self.user_path[i + 1]
            x1, y1 = self.graph.get_position(city1.cityName)
            x2, y2 = self.graph.get_position(city2.cityName)
            
            self.canvas.create_line(x1+100, y1+50, x2+100, y2+50,
                                  fill="#f39c12", width=4, tags="user_path",
                                  arrow=tk.LAST, arrowshape=(16, 20, 6))
    
    def update_status(self):
        """Update the status display"""
        path_names = [city.cityName for city in self.user_path]
        
        # Check if goal reached
        reached_goal = (self.current_city == self.goal_city)
        goal_marker = " [GOAL]" if reached_goal else ""
        
        status_text = (f"YOUR PATH:\n"
                      f"{' -> '.join(path_names)}{goal_marker}\n\n"
                      f"Current: {self.current_city.cityName}\n"
                      f"Goal: {self.goal_city.cityName}\n\n"
                      f"Distance: {self.user_distance}\n"
                      f"Coins Used: {self.user_coins}/{self.max_coins}\n"
                      f"Remaining: {self.max_coins - self.user_coins}\n\n")
        
        if reached_goal:
            status_text += "Goal reached!\nClick Submit to compare!"
        else:
            status_text += "Keep building your path..."
        
        self.result_label.config(text=status_text)
    
    def undo_move(self):
        """Undo the last move"""
        if len(self.user_path) <= 1:
            messagebox.showinfo("Cannot Undo", "You're at the starting city!")
            return
        
        # Remove last city and recalculate
        last_city = self.user_path.pop()
        self.current_city = self.user_path[-1]
        
        # Recalculate distance and coins
        self.user_distance = 0
        self.user_coins = 0
        for i in range(len(self.user_path) - 1):
            edge_info = self.user_path[i].roads[self.user_path[i + 1]]
            self.user_distance += edge_info['distance']
            self.user_coins += edge_info['coins']
        
        self.update_status()
        self.draw_graph()
        self.draw_user_path()
    
    def submit_path(self):
        """Submit the user's path and show comparison"""
        if self.current_city != self.goal_city:
            result = messagebox.askyesno("Path Incomplete", 
                                        f"You haven't reached {self.goal_city.cityName} yet!\n\n"
                                        f"Do you want to submit anyway?")
            if not result:
                return
        
        self.game_mode = "finished"
        self.submit_btn.config(state="disabled")
        self.undo_btn.config(state="disabled")
        
        # Show completion message
        path_names = [city.cityName for city in self.user_path]
        
        if self.current_city == self.goal_city:
            completion_text = (f"PATH SUBMITTED!\n\n"
                              f"Your Path:\n{' -> '.join(path_names)}\n\n"
                              f"Your Distance: {self.user_distance}\n"
                              f"Your Coins: {self.user_coins}\n\n"
                              f"Goal reached!\n\n"
                              f"Click 'Show AI Solution'\nto compare!")
        else:
            completion_text = (f"PATH SUBMITTED!\n\n"
                              f"Your Path:\n{' -> '.join(path_names)}\n\n"
                              f"Your Distance: {self.user_distance}\n"
                              f"Your Coins: {self.user_coins}\n\n"
                              f"Did not reach goal!\n\n"
                              f"Click 'Show AI Solution'\nto see optimal path!")
        
        self.result_label.config(text=completion_text)
    
    def show_ai_solution(self):
        """Show the AI's optimal solution"""
        if self.game_mode == "setup":
            messagebox.showinfo("Start Game First", "Please start the game first!")
            return
        
        self.game_mode = "comparing"
        
        # Run A* algorithm
        ai_path, ai_distance, ai_coins = self.pathfinder.a_star_with_coins(
            self.start_city, self.goal_city, self.max_coins)
        
        if ai_path is None:
            messagebox.showerror("No Solution", "AI couldn't find a path within coin budget!")
            return
        
        # Draw AI path
        self.draw_graph()
        self.draw_user_path()  # Draw user path first (orange)
        
        # Draw AI path (green)
        for i in range(len(ai_path) - 1):
            city1 = ai_path[i]
            city2 = ai_path[i + 1]
            x1, y1 = self.graph.get_position(city1.cityName)
            x2, y2 = self.graph.get_position(city2.cityName)
            
            self.canvas.create_line(x1+100, y1+50, x2+100, y2+50,
                                  fill="#27ae60", width=3, tags="ai_path",
                                  dash=(10, 5))
        
        # Compare results
        user_path_names = [city.cityName for city in self.user_path]
        ai_path_names = [city.cityName for city in ai_path]
        
        # Check if user reached goal
        reached_goal = (self.current_city == self.goal_city)
        
        comparison_text = (f"COMPARISON:\n\n"
                          f"YOUR PATH:\n{' -> '.join(user_path_names)}\n"
                          f"Distance: {self.user_distance}\n"
                          f"Coins: {self.user_coins}\n")
        
        if not reached_goal:
            comparison_text += f"Status: Incomplete\n"
        
        comparison_text += (f"\nAI OPTIMAL PATH:\n{' -> '.join(ai_path_names)}\n"
                          f"Distance: {ai_distance}\n"
                          f"Coins: {ai_coins}\n\n")
        
        if not reached_goal:
            comparison_text += "You didn't reach the goal.\nTry again!"
        else:
            # Calculate difference
            distance_diff = self.user_distance - ai_distance
            coins_diff = self.user_coins - ai_coins
            
            if distance_diff == 0 and coins_diff == 0:
                comparison_text += "PERFECT! Optimal path!"
            elif distance_diff == 0:
                comparison_text += f"Same distance!\n(But used {coins_diff} more coins)"
            elif distance_diff > 0 and distance_diff <= 100:
                comparison_text += f"Close! Only {distance_diff} longer"
            elif distance_diff > 0:
                comparison_text += f"AI saved {distance_diff} distance\nand {coins_diff} coins!"
            else:
                comparison_text += f"You found a shorter path!\n(Used {abs(coins_diff)} extra coins)"
        
        self.result_label.config(text=comparison_text)
        
        # Add legend
        legend_y = 20
        self.canvas.create_line(20, legend_y, 60, legend_y, fill="#f39c12", width=4)
        self.canvas.create_text(120, legend_y, text="Your Path", fill="#f39c12", 
                              font=("Arial", 10, "bold"), anchor=tk.W)
        
        self.canvas.create_line(20, legend_y+25, 60, legend_y+25, fill="#27ae60", 
                              width=3, dash=(10, 5))
        self.canvas.create_text(120, legend_y+25, text="AI Optimal Path", fill="#27ae60", 
                              font=("Arial", 10, "bold"), anchor=tk.W)
    
    def reset_game(self):
        """Reset the game"""
        self.game_mode = "setup"
        self.start_city = None
        self.goal_city = None
        self.current_city = None
        self.user_path = []
        self.user_distance = 0
        self.user_coins = 0
        
        self.start_combo.config(state="readonly")
        self.dest_combo.config(state="readonly")
        self.coins_entry.config(state="normal")
        self.start_game_btn.pack(pady=5, fill=tk.X)
        self.submit_btn.pack_forget()
        self.undo_btn.pack_forget()
        self.ai_solution_btn.pack_forget()
        
        self.instruction_label.config(text="Step 1: Set up your game")
        self.result_label.config(text="Set up your game and click Start!")
        
        self.draw_graph()