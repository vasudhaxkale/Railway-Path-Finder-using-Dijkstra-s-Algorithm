import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import folium
import webbrowser

# Indian railway stations graph with real distances (in kilometers) and costs (in INR)
graph = {
    'New Delhi': {'Agra': {'distance': 200, 'cost': 300}, 'Jaipur': {'distance': 280, 'cost': 420}},
    'Agra': {'New Delhi': {'distance': 200, 'cost': 300}, 'Jaipur': {'distance': 240, 'cost': 360}, 'Lucknow': {'distance': 330, 'cost': 495}},
    'Jaipur': {'New Delhi': {'distance': 280, 'cost': 420}, 'Agra': {'distance': 240, 'cost': 360}, 'Udaipur': {'distance': 650, 'cost': 975}, 'Jodhpur': {'distance': 600, 'cost': 900}},
    'Lucknow': {'New Delhi': {'distance': 500, 'cost': 750}, 'Agra': {'distance': 330, 'cost': 495}, 'Varanasi': {'distance': 320, 'cost': 480}},
    'Udaipur': {'Jaipur': {'distance': 650, 'cost': 975}, 'Jodhpur': {'distance': 250, 'cost': 375}},
    'Varanasi': {'Lucknow': {'distance': 320, 'cost': 480}, 'Patna': {'distance': 230, 'cost': 345}},
    'Jodhpur': {'Jaipur': {'distance': 600, 'cost': 900}, 'Udaipur': {'distance': 250, 'cost': 375}},
    'Patna': {'Varanasi': {'distance': 230, 'cost': 345}, 'Kolkata': {'distance': 600, 'cost': 900}},
    'Kolkata': {'Patna': {'distance': 600, 'cost': 900}, 'Howrah': {'distance': 15, 'cost': 50}},
    'Mumbai': {'Pune': {'distance': 150, 'cost': 225}, 'Nashik': {'distance': 170, 'cost': 255}},
    'Pune': {'Mumbai': {'distance': 150, 'cost': 225}, 'Nashik': {'distance': 210, 'cost': 315}},
    'Nashik': {'Mumbai': {'distance': 170, 'cost': 255}, 'Pune': {'distance': 210, 'cost': 315}},
    'Howrah': {'Kolkata': {'distance': 15, 'cost': 50}}
}

# Coordinates of each station
station_coordinates = {
    'New Delhi': [28.6139, 77.2090],
    'Agra': [27.1767, 78.0081],
    'Jaipur': [26.9124, 75.7873],
    'Lucknow': [26.8467, 80.9462],
    'Udaipur': [24.5854, 73.7125],
    'Varanasi': [25.3176, 82.9739],
    'Jodhpur': [26.2389, 73.0243],
    'Patna': [25.5941, 85.1376],
    'Kolkata': [22.5726, 88.3639],
    'Mumbai': [19.0760, 72.8777],
    'Pune': [18.5204, 73.8567],
    'Nashik': [19.9975, 73.7898],
    'Howrah': [22.5958, 88.2636]
}

# Dijkstra's Algorithm to calculate the shortest path and stores it
def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    costs = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    distances[start] = 0
    costs[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == end:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor, data in graph[current_node].items():
            distance = current_distance + data['distance']
            cost = costs[current_node] + data['cost']

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                costs[neighbor] = cost
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    # Reconstruct the shortest path achieved
    path = []
    node = end
    while node:
        path.insert(0, node)
        node = previous_nodes[node]

    return distances[end], costs[end], path

# Function to show the shortest path in a messagebox of individual paths
def show_path():
    start = start_station.get()
    end = end_station.get()

    if not start or not end:
        messagebox.showerror("Input Error", "Please select both start and end stations.")
        return

    distance, cost, path = dijkstra(graph, start, end)
    if not path:
        messagebox.showerror("Error", "No path found between the selected stations.")
    else:
        messagebox.showinfo("Shortest Path", f"Shortest path: {' -> '.join(path)}")

# Function to show the cost and distance in a messagebox of total path
def show_cost_info():
    start = start_station.get()
    end = end_station.get()

    if not start or not end:
        messagebox.showerror("Input Error", "Please select both start and end stations.")
        return

    distance, cost, path = dijkstra(graph, start, end)
    if not path:
        messagebox.showerror("Error", "No path found between the selected stations.")
    else:
        messagebox.showinfo("Cost and Distance", f"Total Distance: {distance} km\nTotal Cost: INR {cost}")

# Function to show station info in a messagebox(lat and long)
def show_station_info():
    start = start_station.get()
    if not start:
        messagebox.showerror("Input Error", "Please select a station.")
    else:
        messagebox.showinfo("Station Info", f"Coordinates for {start}: {station_coordinates[start]}")

# Function to generate and display the map with the shortest path
def show_map():
    start = start_station.get()
    end = end_station.get()

    if not start or not end:
        messagebox.showerror("Input Error", "Please select both start and end stations.")
        return

    distance, cost, path = dijkstra(graph, start, end)
    if not path:
        messagebox.showerror("Error", "No path found between the selected stations.")
        return

    # Create a folium map centered at the midpoint of the start and end stations
    map_center = [(station_coordinates[start][0] + station_coordinates[end][0]) / 2,
                  (station_coordinates[start][1] + station_coordinates[end][1]) / 2]
    railway_map = folium.Map(location=map_center, zoom_start=6)

    # Add markers and draw lines for the shortest path
    for i, station in enumerate(path):
        folium.Marker(station_coordinates[station], popup=station, icon=folium.Icon(color='green' if i == 0 else 'red' if i == n(path) - 1 else 'blue')).add_to(railway_map)
        if i < len(path) - 1:
            folium.PolyLine([station_coordinates[path[i]], station_coordinates[path[i+1]]], color="blue", weight=2.5).add_to(railway_map)

    # Save the map as an HTML file and open it in the web browser
    map_file = 'railway_map.html'
    railway_map.save(map_file)
    webbrowser.open(map_file)

# Function to reset the inputs
def reset():
    start_station.set('')  # Clear start station selection
    end_station.set('')    # Clear end station selection

# Create the main window
root = tk.Tk()
root.title("Railway Path Finder")
root.geometry("600x550")
root.configure(bg="#e0f7fa")  # Background color

# Title Label
title_label = tk.Label(root, text="Find Railway Paths Between Stations", bg="#e0f7fa", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Frame for input99
input_frame = tk.Frame(root, bg="#e0f7fa")
input_frame.pack(pady=20)

# Labels and dropdowns for start and end stations
tk.Label(input_frame, text="Start Station:", bg="#e0f7fa", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
start_station = ttk.Combobox(input_frame, values=list(graph.keys()), width=40)
start_station.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame, text="End Station:", bg="#e0f7fa", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
end_station = ttk.Combobox(input_frame, values=list(graph.keys()), width=40)
end_station.grid(row=1, column=1, padx=10, pady=5)

# Buttons frame
button_frame = tk.Frame(root, bg="#e0f7fa")
button_frame.pack(pady=10)

# Button to show the shortest path
path_button = tk.Button(button_frame, text="Show Path", command=show_path, bg="#4caf50", fg="white", font=("Arial", 12))
path_button.grid(row=0, column=0, padx=10)

# Button to show cost and distance info
cost_button = tk.Button(button_frame, text="Show Cost", command=show_cost_info, bg="#ff9800", fg="white", font=("Arial", 12))
cost_button.grid(row=0, column=1, padx=10)

# Button to show station info
station_info_button = tk.Button(button_frame, text="Station Info", command=show_station_info, bg="#ff9800", fg="white", font=("Arial", 12))
station_info_button.grid(row=0, column=2, padx=10)

# Button to show the map
map_button = tk.Button(button_frame, text="Show Map", command=show_map, bg="#2196F3", fg="white", font=("Arial", 12))
map_button.grid(row=0, column=3, padx=10)

# Button to reset the form
reset_button = tk.Button(button_frame, text="Reset", command=reset, bg="#2196F3", fg="white", font=("Arial", 12))
reset_button.grid(row=0, column=4, padx=10)

# Button to exit the application
exit_button = tk.Button(button_frame, text="Exit", command=root.quit, bg="#f44336", fg="white", font=("Arial", 12))
exit_button.grid(row=0, column=5, padx=10)

# Run the Tkinter event loop
root.mainloop()
