# main.py
import tkinter as tk
from graph import create_sample_graph
from gui import PathFinderGUI

def main():
    # Create the graph
    graph = create_sample_graph()
    
    # Create the main window
    root = tk.Tk()
    
    # Create the GUI
    app = PathFinderGUI(root, graph)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()