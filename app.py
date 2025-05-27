from flask import Flask, render_template, request
import itertools

app = Flask(__name__)

# List of cities and their distances (graph) for Dijkstra and TSP
cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']

graph = {
    'Delhi': {'Mumbai': 1500, 'Bangalore': 2000, 'Chennai': 2100, 'Kolkata': 1300, 'Hyderabad': 1700, 'Pune': 1600, 'Ahmedabad': 1200, 'Jaipur': 300, 'Lucknow': 500},
    'Mumbai': {'Delhi': 1500, 'Bangalore': 1000, 'Chennai': 1300, 'Kolkata': 1900, 'Hyderabad': 660, 'Pune': 200, 'Ahmedabad': 550, 'Jaipur': 1150, 'Lucknow': 1450},
    'Bangalore': {'Delhi': 2000, 'Mumbai': 1000, 'Chennai': 350, 'Kolkata': 1800, 'Hyderabad': 650, 'Pune': 1500, 'Ahmedabad': 1800, 'Jaipur': 1700, 'Lucknow': 1700},
    'Chennai': {'Delhi': 2100, 'Mumbai': 1300, 'Bangalore': 350, 'Kolkata': 1600, 'Hyderabad': 700, 'Pune': 1400, 'Ahmedabad': 1800, 'Jaipur': 2000, 'Lucknow': 2000},
    'Kolkata': {'Delhi': 1300, 'Mumbai': 1900, 'Bangalore': 1800, 'Chennai': 1600, 'Hyderabad': 1200, 'Pune': 1700, 'Ahmedabad': 1400, 'Jaipur': 1700, 'Lucknow': 1000},
    'Hyderabad': {'Delhi': 1700, 'Mumbai': 660, 'Bangalore': 650, 'Chennai': 700, 'Kolkata': 1200, 'Pune': 550, 'Ahmedabad': 800, 'Jaipur': 1400, 'Lucknow': 1400},
    'Pune': {'Delhi': 1600, 'Mumbai': 200, 'Bangalore': 1500, 'Chennai': 1400, 'Kolkata': 1700, 'Hyderabad': 550, 'Ahmedabad': 700, 'Jaipur': 1300, 'Lucknow': 1600},
    'Ahmedabad': {'Delhi': 1200, 'Mumbai': 550, 'Bangalore': 1800, 'Chennai': 1800, 'Kolkata': 1400, 'Hyderabad': 800, 'Pune': 700, 'Jaipur': 500, 'Lucknow': 1500},
    'Jaipur': {'Delhi': 300, 'Mumbai': 1150, 'Bangalore': 1700, 'Chennai': 2000, 'Kolkata': 1700, 'Hyderabad': 1400, 'Pune': 1300, 'Ahmedabad': 500, 'Lucknow': 800},
    'Lucknow': {'Delhi': 500, 'Mumbai': 1450, 'Bangalore': 1700, 'Chennai': 2000, 'Kolkata': 1000, 'Hyderabad': 1400, 'Pune': 1600, 'Ahmedabad': 1500, 'Jaipur': 800}
}

def dijkstra(start, end):
    unvisited = {city: float('inf') for city in cities}
    unvisited[start] = 0
    visited = {}
    predecessors = {}

    while unvisited:
        min_city = min(unvisited, key=unvisited.get)
        if unvisited[min_city] == float('inf'):
            break
        for neighbor, distance in graph[min_city].items():
            if neighbor not in visited:
                new_dist = unvisited[min_city] + distance
                if new_dist < unvisited[neighbor]:
                    unvisited[neighbor] = new_dist
                    predecessors[neighbor] = min_city
        visited[min_city] = unvisited[min_city]
        unvisited.pop(min_city)

    path = []
    current_city = end
    while current_city != start:
        path.insert(0, current_city)
        current_city = predecessors[current_city]
    path.insert(0, start)
    return visited[end], path

def tsp():
    min_cost = float('inf')
    min_path = []
    for perm in itertools.permutations(cities):
        cost = 0
        for i in range(len(perm) - 1):
            cost += graph[perm[i]][perm[i+1]]
        cost += graph[perm[-1]][perm[0]]  # Complete the cycle
        if cost < min_cost:
            min_cost = cost
            min_path = perm
    return min_cost, min_path

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        departure_city = request.form["departure"]
        arrival_city = request.form["arrival"]
        algorithm = request.form["algorithm"]

        if algorithm == "Dijkstra":
            cost, path = dijkstra(departure_city, arrival_city)
            result = f"Total Cost: {cost}\nPath: {' → '.join(path)}"
        elif algorithm == "TSP":
            cost, path = tsp()
            result = f"Total Cost: {cost}\nPath: {' → '.join(path)}"
        return render_template("results.html", result=result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
