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
    
    def create_widgets(self):
        
        # Configure ttk Combobox style
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme for better customization
        
        # Configure Combobox colors
        style.configure('TCombobox',
                       fieldbackground='white',
                       background='#EBD4CB',  # Arrow button background
                       foreground='#2C0603',  # Text color
                       arrowcolor='#2C0603',  # Arrow color
                       bordercolor='#890620',
                       lightcolor='#EBD4CB',
                       darkcolor='#890620')
        
        style.map('TCombobox',
                 fieldbackground=[('readonly', 'white')],
                 selectbackground=[('readonly', '#B6465F')],
                 selectforeground=[('readonly', 'white')],
                 arrowcolor=[('disabled', '#95a5a6')])
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)


        # Left Control Panel where user inputs are
        control_frame = tk.Frame(self.root, bg="#2C0603")
        control_frame.grid(row=0, column=0, sticky="nsew")

        # Right Display Panel for graph visualization
        self.display_frame = tk.Frame(self.root, bg="#2C0603")
        self.display_frame.grid(row=0, column=1, sticky="nsew")

        content = tk.Frame(control_frame, bg="#2C0603", padx=5, pady=5)
        content.pack(fill="both", expand=True)


        title = tk.Label(
            content,
            text="Path Finder Game",
            font=("Almendra", 32, "bold"),
            bg="#2C0603",
            fg="white"
        )
        title.pack(pady=(0, 5))


        form_frame = tk.Frame(content, bg="#2C0603")
        form_frame.pack(fill="both", expand=True)


        form_frame.grid_columnconfigure(0, weight=0)  # labels
        form_frame.grid_columnconfigure(1, weight=0)  # inputs

        # Common input settings
        input_width = 40
        input_font = ("Almendra", 15)

        # Start City
        tk.Label(form_frame, text="Start City:", font=("Almendra", 25),
                bg="#2C0603", fg="white").grid(row=0, column=0, sticky="", pady=8)
        self.start_var = tk.StringVar(value="Select Node")
        self.start_combo = ttk.Combobox(form_frame, textvariable=self.start_var,
                                        values=self.graph.get_city_names(),
                                        state="readonly", width=input_width)
        self.start_combo.config(font=input_font)
        self.start_combo.grid(row=0, column=1, pady=8, padx=(10,0))

        # Destination City 
        tk.Label(form_frame, text="Destination:", font=("Almendra", 25),
                bg="#2C0603", fg="white").grid(row=1, column=0, sticky="", pady=8)
        self.dest_var = tk.StringVar(value="Select Node")
        self.dest_combo = ttk.Combobox(form_frame, textvariable=self.dest_var,
                                    values=self.graph.get_city_names(),
                                    state="readonly", width=input_width)
        self.dest_combo.config(font=input_font)
        self.dest_combo.grid(row=1, column=1, pady=8, padx=(10,0))

        # Coin Budget
        tk.Label(form_frame, text="Coin Budget:", font=("Almendra", 25),
                bg="#2C0603", fg="white").grid(row=2, column=0, sticky="", pady=8)
        self.coins_var = tk.StringVar(value="25")
        self.coins_entry = tk.Entry(form_frame, textvariable=self.coins_var,
                                    font=input_font, width=input_width)
        self.coins_entry.grid(row=2, column=1, pady=8, padx=(10,0))


        # Buttons Frame
        buttons_frame = tk.Frame(control_frame, bg="#2C0603")
        buttons_frame.pack(pady=5)
        
        # Start Game Button
        self.start_game_btn = tk.Button(buttons_frame, text="Start Game", 
                                        font=("Almendra", 20, "bold"),
                                        bg="#EBD4CB", fg="#2C0603", 
                                        command=self.start_game,
                                        relief=tk.FLAT, padx=15, pady=8, width=20)
        self.start_game_btn.pack(pady=5)
        
        # Submit Path Button (hidden initially)
        self.submit_btn = tk.Button(buttons_frame, text="Submit My Path", 
                                    font=("Almendra", 20, "bold"),
                                    bg="#EBD4CB", fg="#2C0603", 
                                    command=self.submit_path,
                                    relief=tk.FLAT, padx=15, pady=8, width=20)
        
        # Undo Last Move Button (hidden initially)
        self.undo_btn = tk.Button(buttons_frame, text="Undo Last Move", 
                                  font=("Almendra", 20),
                                  bg="#EBD4CB", fg="#2C0603", 
                                  command=self.undo_move,
                                  relief=tk.FLAT, padx=15, pady=6, width=20)
        
        # Show AI Solution Button (hidden initially)
        self.ai_solution_btn = tk.Button(buttons_frame, text="Show AI Solution", 
                                         font=("Almendra", 20),
                                         bg="#EBD4CB", fg="#2C0603", 
                                         command=self.show_ai_solution,
                                         relief=tk.FLAT, padx=15, pady=7, width=20)
        
        # Reset Button
        self.reset_btn = tk.Button(buttons_frame, text="Reset Game", 
                                   font=("Almendra", 20),
                                   bg="#EBD4CB", fg="#2C0603", 
                                   command=self.reset_game,
                                   relief=tk.FLAT, padx=15, pady=7, width=20)
        self.reset_btn.pack(pady=5)

 
        # Info Display with Scrollbar
        self.info_frame = tk.Frame(control_frame, bg="#EBD4CB", relief=tk.GROOVE, bd=2, width=400, height=400)
        self.info_frame.pack(pady=5, expand=True)

        self.info_frame.pack_propagate(False)

        
        tk.Label(self.info_frame, text="Game Status", font=("Almendra", 25, "bold"),
                bg="#EBD4CB", fg="#2C0603").pack(pady=8)
        
        # Create a frame to hold the text widget and scrollbar
        text_container = tk.Frame(self.info_frame, bg="#EBD4CB")
        text_container.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(text_container, bg="#EBD4CB", troughcolor="#EBD4CB")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Replace Label with Text widget for scrolling
        self.result_text = tk.Text(text_container, font=("Almendra", 15),
                                   bg="#EBD4CB", fg="#2C0603", 
                                   wrap=tk.WORD, relief=tk.FLAT,
                                   yscrollcommand=scrollbar.set,
                                   state=tk.DISABLED)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.result_text.yview)
        
        # Initial text
        self.update_result_text("Set up your game and click Start!")
        

        # Canvas for visualization — put it inside the right display panel (self.display_frame)
        canvas_frame = tk.Frame(self.display_frame, bg="#2C0603")
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="#2C0603", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bind clicks
        self.canvas.bind("<Button-1>", self.on_city_click)

        # Draw initial graph
        self.draw_graph()


    def update_result_text(self, text):
        """Helper method to update the scrollable text widget"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, text)
        self.result_text.config(state=tk.DISABLED)
        # Scroll to top
        self.result_text.see(1.0)
    
    def draw_graph(self):
        self.canvas.delete("all")

        xs, ys = [], []
        for name in self.graph.get_city_names():
            x, y = self.graph.get_position(name)
            xs.append(x)
            ys.append(y)

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        graph_w = max_x - min_x
        graph_h = max_y - min_y

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w < 10 or canvas_h < 10:
            self.canvas.update_idletasks()
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()

        margin = 40
        usable_w = canvas_w - margin * 2
        usable_h = canvas_h - margin * 2
        scale_x = usable_w / graph_w if graph_w > 0 else 1
        scale_y = usable_h / graph_h if graph_h > 0 else 1
        SCALE = min(scale_x, scale_y)

        scaled_w = graph_w * SCALE
        scaled_h = graph_h * SCALE
        offset_x = (canvas_w - scaled_w) // 2 - min_x * SCALE
        offset_y = (canvas_h - scaled_h) // 2 - min_y * SCALE


        # Store scaled positions in the class
        self.scaled_positions = {}
        for city_name in self.graph.get_city_names():
            x, y = self.graph.get_position(city_name)
            sx = x * SCALE + offset_x
            sy = y * SCALE + offset_y
            self.scaled_positions[city_name] = (sx, sy)


        # Draw edges
        for city_name, city in self.graph.cities.items():
            sx1, sy1 = self.scaled_positions[city_name]

            for neighbor, edge_info in city.roads.items():
                neighbor_name = neighbor.cityName
                if city_name < neighbor_name:
                    sx2, sy2 = self.scaled_positions[neighbor_name]

                    self.canvas.create_line(
                        sx1, sy1, sx2, sy2,
                        fill="white", width=2
                    )

                    mx = (sx1 + sx2) / 2
                    my = (sy1 + sy2) / 2

                    self.canvas.create_text(
                        mx, my - 15,
                        text=f"Distance: {edge_info['distance']}",
                        fill="#EBD4CB",
                        font=("Almendra", 15)
                    )
                    self.canvas.create_text(
                        mx, my + 12,
                        text=f"Coins: {edge_info['coins']}",
                        fill="#DAA094",
                        font=("Almendra", 15, "bold")
                    )


        # Draw cities
        for city_name in self.graph.get_city_names():
            sx, sy = self.scaled_positions[city_name]
            city = self.graph.get_city(city_name)

            if self.game_mode in ["playing", "finished", "comparing"]:
                if city == self.current_city:
                    color = "#890620"; outline = "#2C0703"; text_color = "white"
                elif city == self.start_city:
                    color = "#B6465F"; outline = "#890620"; text_color = "white"
                elif city == self.goal_city:
                    color = "#2C0703"; outline = "#890620"; text_color = "white"
                elif city in [self.graph.get_city(c.cityName) for c in self.user_path]:
                    color = "#DA9F93"; outline = "#B6465F"; text_color = "white"
                else:
                    color = "#EBD4CB"; outline = "#DA9F93"; text_color = "#2C0603"
            else:
                color = "#B6465F"; outline = "#890620"; text_color = "black"

            R = max(10, 20 * SCALE)
            self.canvas.create_oval(
                sx - R, sy - R, sx + R, sy + R,
                fill=color, outline=outline, width=3
            )
            self.canvas.create_text(
                sx, sy,
                text=city_name,
                fill=text_color,
                font=("Almendra", int(17 * SCALE), "bold")
            )

            heuristic = city.get_heuristic()
            self.canvas.create_text(
                sx, sy + R + 15,
                text=f"h={int(heuristic)}",
                fill="#B6465F",
                font=("Almendra", int(20 * SCALE), "bold")
            )


    def start_game(self):
        # Initialize the game
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
            
            self.update_status()
            self.draw_graph()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid coin budget!")
    
    
    
    def on_city_click(self, event):
        if self.game_mode != "playing":
            return
        
        clicked_city = None
        
        # Use the same scaling as draw_graph
        xs, ys = [], []
        for name in self.graph.get_city_names():
            x, y = self.graph.get_position(name)
            xs.append(x)
            ys.append(y)

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        graph_w = max_x - min_x
        graph_h = max_y - min_y

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w < 10 or canvas_h < 10:
            self.canvas.update_idletasks()
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()

        margin = 40
        usable_w = canvas_w - margin * 2
        usable_h = canvas_h - margin * 2
        scale_x = usable_w / graph_w if graph_w > 0 else 1
        scale_y = usable_h / graph_h if graph_h > 0 else 1
        SCALE = min(scale_x, scale_y)

        scaled_w = graph_w * SCALE
        scaled_h = graph_h * SCALE
        offset_x = (canvas_w - scaled_w) // 2 - min_x * SCALE
        offset_y = (canvas_h - scaled_h) // 2 - min_y * SCALE

        def T(px, py):
            return px * SCALE + offset_x, py * SCALE + offset_y

        # Now check clicks against scaled positions
        for city_name in self.graph.get_city_names():
            x, y = self.graph.get_position(city_name)
            sx, sy = T(x, y)
            R = max(10, 20 * SCALE)
            if (sx - R <= event.x <= sx + R) and (sy - R <= event.y <= sy + R):
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
                                     f"You only have {self.max_coins - self.user_coins} coins left!\n\n"
                                     f"Try using 'Undo Last Move' to go back.")
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
        # Draw the user's chosen path
        for i in range(len(self.user_path) - 1):
            city1 = self.user_path[i]
            city2 = self.user_path[i + 1]

            # Use scaled positions from draw_graph
            sx1, sy1 = self.scaled_positions[city1.cityName]
            sx2, sy2 = self.scaled_positions[city2.cityName]

            self.canvas.create_line(
                sx1, sy1, sx2, sy2,
                fill="#DA9F93",
                width=4,
                tags="user_path",
                arrow=tk.LAST,
                arrowshape=(16, 20, 6)
            )

    def update_status(self):
        # Update the status display
        path_names = [city.cityName for city in self.user_path]
        
        # Check if goal reached
        reached_goal = (self.current_city == self.goal_city)
        goal_marker = " [GOAL]" if reached_goal else ""
        
        status_text = (f"YOUR PATH:\n"
                      f"{' → '.join(path_names)}{goal_marker}\n\n"
                      f"Current: {self.current_city.cityName}\n"
                      f"Goal: {self.goal_city.cityName}\n\n"
                      f"Distance: {self.user_distance}\n"
                      f"Coins Used: {self.user_coins}/{self.max_coins}\n"
                      f"Remaining: {self.max_coins - self.user_coins}\n\n")
        
        if reached_goal:
            status_text += "Goal reached!\nClick Submit to compare!"
        else:
            status_text += "Keep building your path..."
        
        self.update_result_text(status_text)
    
        
    def undo_move(self):
        # Undo the last move
        if len(self.user_path) <= 1:
            messagebox.showinfo("Cannot Undo", "You're at the starting city!")
            return
        
        # If submitted, re-enable submit button
        if self.game_mode == "finished":
            self.game_mode = "playing"
            self.submit_btn.config(state="normal")
        
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
        # Submit the user's path and show comparison
        if self.current_city != self.goal_city:
            result = messagebox.askyesno("Path Incomplete", 
                                        f"You haven't reached {self.goal_city.cityName} yet!\n\n"
                                        f"Do you want to submit anyway?")
            if not result:
                return
        
        self.game_mode = "finished"
        self.submit_btn.config(state="disabled")
        # Keep undo button enabled so players can go back and try again
        
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
        
        self.update_result_text(completion_text)
    
    def show_ai_solution(self):
        # Show the AI's optimal solution
        if self.game_mode == "setup":
            messagebox.showinfo("Start Game First", "Please start the game first!")
            return

        self.game_mode = "comparing"

        # Run A* algorithm
        ai_path, ai_distance, ai_coins = self.pathfinder.a_star_with_coins(
            self.start_city, self.goal_city, self.max_coins
        )

        if ai_path is None:
            messagebox.showerror("No Solution", "AI couldn't find a path within coin budget!")
            return

        # Compute scaling and offsets 
        xs, ys = [], []
        for name in self.graph.get_city_names():
            x, y = self.graph.get_position(name)
            xs.append(x)
            ys.append(y)

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        graph_w = max_x - min_x
        graph_h = max_y - min_y

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w < 10 or canvas_h < 10:
            self.canvas.update_idletasks()
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()

        margin = 40
        usable_w = canvas_w - margin * 2
        usable_h = canvas_h - margin * 2
        scale_x = usable_w / graph_w if graph_w > 0 else 1
        scale_y = usable_h / graph_h if graph_h > 0 else 1
        SCALE = min(scale_x, scale_y)

        scaled_w = graph_w * SCALE
        scaled_h = graph_h * SCALE
        offset_x = (canvas_w - scaled_w) // 2 - min_x * SCALE
        offset_y = (canvas_h - scaled_h) // 2 - min_y * SCALE

        def T(px, py):
            return px * SCALE + offset_x, py * SCALE + offset_y

        # Draw AI path
        self.draw_graph()
        self.draw_user_path()

        for i in range(len(ai_path) - 1):
            city1 = ai_path[i]
            city2 = ai_path[i + 1]
            x1, y1 = self.graph.get_position(city1.cityName)
            x2, y2 = self.graph.get_position(city2.cityName)
            sx1, sy1 = T(x1, y1)
            sx2, sy2 = T(x2, y2)

            self.canvas.create_line(
                sx1, sy1, sx2, sy2,
                fill="#890620", width=3, tags="ai_path", dash=(10, 5)
            )


        # Compare results and update status
        user_path_names = [city.cityName for city in self.user_path]
        ai_path_names = [city.cityName for city in ai_path]

        reached_goal = (self.current_city == self.goal_city)

        comparison_text = (
            f"COMPARISON:\n\n"
            f"YOUR PATH:\n{' → '.join(user_path_names)}\n"
            f"Distance: {self.user_distance}\n"
            f"Coins: {self.user_coins}\n"
        )

        if not reached_goal:
            comparison_text += "Status: Incomplete\n"

        comparison_text += (
            f"\nAI OPTIMAL PATH:\n{' → '.join(ai_path_names)}\n"
            f"Distance: {ai_distance}\n"
            f"Coins: {ai_coins}\n\n"
        )

        # Add A* calculation showing step-by-step arithmetic
        comparison_text += "="*40 + "\n"
        comparison_text += "A* CALCULATION:\n"
        comparison_text += "f(n) = g(n) + h(n)\n"
        comparison_text += "="*40 + "\n\n"
        
        cumulative_g = 0
        cumulative_coins = 0
        
        for i, city in enumerate(ai_path):
            h = int(city.get_heuristic())
            
            if i == 0:
                # Starting node
                f = 0 + h
                comparison_text += f"Step {i+1}: {city.cityName}\n"
                comparison_text += f"  g(n) = 0 (start)\n"
                comparison_text += f"  h(n) = {h}\n"
                comparison_text += f"  f(n) = 0 + {h} = {f}\n"
                comparison_text += f"  Total Distance: 0\n"
                comparison_text += f"  Total Coins: 0\n\n"
            else:
                # Subsequent nodes - show the calculation
                prev_city = ai_path[i-1]
                edge_info = prev_city.roads[city]
                edge_dist = edge_info['distance']
                edge_coins = edge_info['coins']
                prev_g = cumulative_g
                cumulative_g += edge_dist
                cumulative_coins += edge_coins
                f = cumulative_g + h
                
                comparison_text += f"Step {i+1}: {prev_city.cityName} → {city.cityName}\n"
                comparison_text += f"  Edge: distance={edge_dist}, coins={edge_coins}\n"
                comparison_text += f"  g(n) = {prev_g} + {edge_dist} = {cumulative_g}\n"
                comparison_text += f"  h(n) = {h}\n"
                comparison_text += f"  f(n) = {cumulative_g} + {h} = {f}\n"
                comparison_text += f"  Total Distance: {cumulative_g}\n"
                comparison_text += f"  Total Coins: {cumulative_coins}\n\n"
        
        comparison_text += "="*40 + "\n"
        comparison_text += f"FINAL TOTALS:\n"
        comparison_text += f"Total Distance: {ai_distance}\n"
        comparison_text += f"Total Coins: {ai_coins}\n"
        comparison_text += f"Coins Remaining: {self.max_coins - ai_coins}\n"
        comparison_text += "="*40 + "\n\n"

        if not reached_goal:
            comparison_text += "You didn't reach the goal.\nTry again!"
        else:
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

        self.update_result_text(comparison_text)


        # Add legend
        legend_y = 20
        self.canvas.create_line(20, legend_y, 60, legend_y, fill="#DA9F93", width=4)
        self.canvas.create_text(
            120, legend_y, text="Your Path", fill="#DA9F93", font=("Almendra", 15, "bold"), anchor=tk.W
        )

        self.canvas.create_line(20, legend_y + 25, 60, legend_y + 25, fill="#B6465F", width=3, dash=(10, 5))
        self.canvas.create_text(
            120, legend_y + 25, text="AI Optimal Path", fill="#B6465F", font=("Almendra", 15, "bold"), anchor=tk.W
        )

    
    def reset_game(self):
        # Reset the game
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
        
        self.update_result_text("Set up your game and click Start!")
        
        self.draw_graph()