import heapq
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

class Node:
    def __init__(self, name, parent=None, g_cost=0, h_cost=0):
        self.name = name
        self.parent = parent
        self.g_cost = g_cost  
        self.h_cost = h_cost  
        self.f_cost = g_cost + h_cost 

    def __lt__(self, other):
        return self.f_cost < other.f_cost  

    def path(self):
        node, path = self, []
        while node:
            path.append(node.name)
            node = node.parent
        return path[::-1]

def read_graph_and_heuristics_from_csv(filename):
    df = pd.read_csv(filename)
    graph = {}
    heuristics = {}

    for _, row in df.iterrows():
        src, dest, weight, heuristic = row['Source'], row['Destination'], row['Weight'], row['Heuristic']

        if src not in graph:
            graph[src] = []
        graph[src].append((dest, weight))

        heuristics[src] = heuristic  

    return graph, heuristics

def a_star_search(graph, heuristics, start, goal):
    pq = []
    heapq.heappush(pq, (heuristics.get(start, float('inf')), Node(start, g_cost=0, h_cost=heuristics.get(start, 0))))
    visited = set()
    search_tree = nx.DiGraph()
    goal_node = None
    path_nodes = set()

    while pq:
        _, current = heapq.heappop(pq)

        if current.name in visited:
            continue

        visited.add(current.name)

        if current.parent:
            search_tree.add_edge(current.parent.name, current.name, weight=current.g_cost - current.parent.g_cost)

        print(f"Node: {current.name}, g: {current.g_cost}, h: {current.h_cost}, f: {current.f_cost}, Path: {' -> '.join(current.path())}")

        if current.name == goal:
            goal_node = current
            print("\nGoal reached! Optimal Path:", " -> ".join(current.path()))
            path_nodes = set(current.path())
            break

        for neighbor, weight in graph.get(current.name, []):
            if neighbor not in visited:
                g_cost = current.g_cost + weight
                h_cost = heuristics.get(neighbor, float('inf'))
                heapq.heappush(pq, (g_cost + h_cost, Node(neighbor, current, g_cost, h_cost)))

    if goal_node:
        draw_tree(search_tree, path_nodes)
    else:
        print("\nNo path found to the goal!")
        draw_tree(search_tree, path_nodes)

def draw_tree(tree, path_nodes):
    pos = nx.spring_layout(tree, seed=40, k=2)
    plt.figure(figsize=(12, 10))

    edge_labels = nx.get_edge_attributes(tree, 'weight')

    node_colors = ['lightblue' if node not in path_nodes else 'yellow' for node in tree.nodes()]
    edge_colors = ['blue' if tree[u][v]['weight'] > 0 and (u in path_nodes and v in path_nodes) else 'gray' for u, v in tree.edges()]

    nx.draw(tree, pos, with_labels=True, node_size=1000, node_color=node_colors, font_size=8, font_weight="bold", edge_color=edge_colors, width=2)
    nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels, font_size=10, font_weight="bold")

    plt.title("A* Search Tree with Costs", fontsize=12)
    plt.show()

def menu():
    while True:
        print("\n===== A* Search Algorithm Menu =====")
        print("1. Find Optimal Path (Graph 1: AFS1.csv)")
        print("2. Find Non-Optimal Path (Graph 2: AFS2.csv)")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            graph, heuristics = read_graph_and_heuristics_from_csv("AFS1.csv")
            start = input("Enter the start node: ")
            goal = input("Enter the goal node: ")
            a_star_search(graph, heuristics, start, goal)

        elif choice == '2':
            graph, heuristics = read_graph_and_heuristics_from_csv("AFS2.csv")
            start = input("Enter the start node: ")
            goal = input("Enter the goal node: ")
            a_star_search(graph, heuristics, start, goal)

        elif choice == '3':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select a valid option.")

menu()
