import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Створюємо граф
G = nx.DiGraph()

# Додаємо ребра з пропускною здатністю
edges = [
    (0, 2, 15),  # Джерело 1 -> Проміжний Вузол 1
    (0, 3, 10),  # Джерело 1 -> Проміжний Вузол 2
    (1, 2, 20),  # Джерело 2 -> Проміжний Вузол 1
    (2, 4, 10),  # Проміжний Вузол 1 -> Споживач 1
    (2, 5, 5),   # Проміжний Вузол 1 -> Споживач 2
    (3, 6, 15),  # Проміжний Вузол 2 -> Споживач 3
]

# Додаємо всі ребра до графа
G.add_weighted_edges_from(edges)

# Позиції для малювання графа
pos = {
    0: (0, 2),  # Джерело 1
    1: (0, 0),  # Джерело 2
    2: (2, 2),  # Проміжний Вузол 1
    3: (2, 1),  # Проміжний Вузол 2
    4: (4, 2),  # Споживач 1
    5: (4, 1),  # Споживач 2
    6: (4, 0),  # Споживач 3
}

# Малюємо граф
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=12, font_weight="bold", arrows=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Відображаємо граф
plt.show()

# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()
        
        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    
    return False

# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node
        
        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node
        
        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow

# Матриця пропускної здатності для каналів у мережі (capacity_matrix)
capacity_matrix = [
    [0, 0, 15, 10, 0, 0, 0],  # Джерело 1
    [0, 0, 20, 0, 0, 0, 0],   # Джерело 2
    [0, 0, 0, 0, 10, 5, 0],   # Проміжний Вузол 1
    [0, 0, 0, 0, 0, 0, 15],   # Проміжний Вузол 2
    [0, 0, 0, 0, 0, 0, 0],    # Споживач 1
    [0, 0, 0, 0, 0, 0, 0],    # Споживач 2
    [0, 0, 0, 0, 0, 0, 0]     # Споживач 3
]

source = 0  # Джерело 1
sink = 5    # Споживач 3

print(f"Максимальний потік: {edmonds_karp(capacity_matrix, source, sink)}")

