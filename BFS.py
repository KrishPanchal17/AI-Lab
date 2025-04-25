import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def read_graph_from_csv(BFS):
        df = pd.read_csv(BFS)
        graph = {}
        
        for _, row in df.iterrows():
            src, dest, weight = row['Source'], row['Destination'], row['Weight']
            
            if src not in graph:
                graph[src] = []
            if dest not in graph:
                graph[dest] = []
            
            graph[src].append((dest, weight))
            graph[dest].append((src, weight))
        
        return graph

def bfs(graph, start, goal):
        queue = deque([start])
        visited = set([start])
        parent = {start: None}
        
        while queue:
            node = queue.popleft()
            
            print(f"Visiting Node: {node}")
            
            if node == goal:
                print(f"Goal {goal} found!")
                return reconstruct_path(parent, goal)

            for neighbor, weight in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    queue.append(neighbor)

        print(f"No path found from {start} to {goal}")
        return []

def reconstruct_path(parent, goal):
        path = []
        while goal is not None:
            path.append(goal)
            goal = parent[goal]
        return path[::-1]

def visualize_bfs_tree(graph, path):
        G = nx.Graph()
        for node in graph:
            for neighbor, weight in graph[node]:
                G.add_edge(node, neighbor, weight=weight)
        
        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(12, 10))

        edge_labels = nx.get_edge_attributes(G, 'weight')
        node_colors = ['yellow' if node in path else 'lightblue' for node in G.nodes()]
        edge_colors = ['blue' if (u in path and v in path) else 'gray' for u, v in G.edges()]

        nx.draw(G, pos, with_labels=True, node_size=1000, node_color=node_colors, font_size=12, font_weight="bold", edge_color=edge_colors, width=2)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

        plt.title("Breadth First Search Tree", fontsize=16)
        plt.show()

graph = read_graph_from_csv('BFS.csv')

start = input("Enter the start node: ")
goal = input("Enter the goal node: ")

print("\nBreadth First Search Traversal:")
bfs_path = bfs(graph, start, goal)

if bfs_path:
        print(f"\nBFS Path from {start} to {goal}: {' -> '.join(bfs_path)}")
        visualize_bfs_tree(graph, bfs_path)
else:
        print("No path found!")
