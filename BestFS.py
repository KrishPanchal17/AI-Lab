import heapq
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

class Node:
    def __init__(self, name, parent=None, cost=0):
        self.name = name
        self.parent = parent
        self.cost = cost 

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
        
        heuristics[dest] = heuristic
        
    return graph, heuristics

def best_first_search(graph, heuristic, start, goal):
    pq = []
    heapq.heappush(pq, (heuristic.get(start, float('inf')), Node(start, cost=0)))  
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
            search_tree.add_edge(current.parent.name, current.name, weight=current.cost)

        print(f"Node: {current.name}, Cost: {current.cost}, Path: {' -> '.join(current.path())}")

        if current.name == goal:
            goal_node = current
            print("\nGoal reached! Path:", " -> ".join(current.path()))
            path_nodes = set(current.path()) 
            break

        for neighbor, weight in graph.get(current.name, []):
            if neighbor not in visited:
                new_cost = current.cost + weight
                heapq.heappush(pq, (heuristic.get(neighbor, float('inf')), Node(neighbor, current, new_cost)))

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
    
    plt.title("Best First Search Tree with Costs", fontsize=12)
    plt.show()

graph, heuristic = read_graph_and_heuristics_from_csv("BestFS.csv")

start = input("Enter the start node: ")
goal = input("Enter the goal node: ")

print("\nBest First Search Tree:")
best_first_search(graph, heuristic, start, goal)
