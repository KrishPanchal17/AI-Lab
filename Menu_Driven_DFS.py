import csv
import networkx as nx
import matplotlib.pyplot as plt

def load_graph_from_csv(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for Source, Dest in reader:
            if Source not in graph:
                graph[Source] = []
            graph[Source].append(Dest)
            if Dest not in graph:
                graph[Dest] = []
    return graph

def dfs_recursive(graph, node, visited, result):
    visited.add(node)
    result.append(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, result)

def dfs_iterative(graph, start):
    stack = [start]
    visited = set()
    result = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    return result

def visualize_tree(traversal_order, title):
    tree = nx.DiGraph()
    for i in range(len(traversal_order) - 1):
        tree.add_edge(traversal_order[i], traversal_order[i + 1])

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(tree, seed=42)  # Fixed layout for consistency
    nx.draw(tree, pos, with_labels=True, node_color="lightgreen", node_size=800, font_size=10, edge_color="black")
    plt.title(title)
    plt.show()

def main():
    file_path = "DFS.csv"
    graph = load_graph_from_csv(file_path)
    print("Graph loaded successfully!")

    while True:
        print("\nMenu:")
        print("1. Perform and Visualize Recursive DFS")
        print("2. Perform and Visualize Iterative DFS")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            start_node = input("Enter the start node for Recursive DFS: ")
            visited = set()
            result = []
            if start_node in graph:
                dfs_recursive(graph, start_node, visited, result)
                print("Recursive DFS Traversal:", result)
                visualize_tree(result, "Recursive DFS Tree")
            else:
                print("Invalid start node!")
        elif choice == '2':
            start_node = input("Enter the start node for Iterative DFS: ")
            if start_node in graph:
                result = dfs_iterative(graph, start_node)
                print("Iterative DFS Traversal:", result)
                visualize_tree(result, "Iterative DFS Tree")
            else:
                print("Invalid start node!")
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
