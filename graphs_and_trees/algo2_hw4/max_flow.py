import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from rich import print


# Створюємо граф
G = nx.DiGraph()
# Додаємо ребра з пропускною здатністю
edges = [
    ("Terminal_1", "Content_1", 25),
    ("Terminal_1", "Content_2", 20),
    ("Terminal_1", "Content_3", 15),

    ("Terminal_2", "Content_3", 15),
    ("Terminal_2", "Content_4", 30),
    ("Terminal_2", "Content_2", 10),

    ("Content_1", "Store_1", 15),
    ("Content_1", "Store_2", 10),
    ("Content_1", "Store_3", 20),

    ("Content_2", "Store_4", 15),
    ("Content_2", "Store_5", 10),
    ("Content_2", "Store_6", 25),

    ("Content_3", "Store_7", 20),
    ("Content_3", "Store_8", 15),
    ("Content_3", "Store_9", 10),

    ("Content_4", "Store_10", 20),
    ("Content_4", "Store_11", 10),
    ("Content_4", "Store_12", 15),
    ("Content_4", "Store_13", 5),
    ("Content_4", "Store_14", 10)
    ]
# Додаємо ребра з вагами (пропускною здатністю)
for from_node, to_node, capacity in edges:
    G.add_edge(from_node, to_node, capacity=capacity)

# Позиціі для візуалізації
pos = {
    "Terminal_1": (2, 0),
    "Terminal_2": (10, 0),
    "Content_1": (4, 2),
    "Content_2": (8, 2),
    "Content_3": (4, -2),
    "Content_4": (8, -2),
    "Store_1": (0, 4),
    "Store_2": (2, 4),
    "Store_3": (4, 4),
    "Store_4": (6, 4),
    "Store_5": (8, 4),
    "Store_6": (10, 4),
    "Store_7": (0, -4),
    "Store_8": (2, -4),
    "Store_9": (4, -4),
    "Store_10": (6, -4),
    "Store_11": (8, -4),
    "Store_12": (10, -4),
    "Store_13": (12, -4),
    "Store_14": (14, -4)
}

# Візуалізація графа
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=12, font_weight="bold", arrows=True)
labels = nx.get_edge_attributes(G, 'capacity')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Відображаємо граф
plt.show()

edges_source = [
    ("Source", "Terminal_1", 60),
    ("Source", "Terminal_2", 55)
]

edges_sink = []
for i in range(1, 15):
    edges_sink.append((f"Store_{i}", "Sink", 115))

# Додаємо ребра від Source до Terminal та від Store до Sink
for from_node, to_node, capacity in edges_source:
    G.add_edge(from_node, to_node, capacity=capacity)
for from_node, to_node, capacity in edges_sink:
    G.add_edge(from_node, to_node, capacity=capacity)

# Обчислюємо максимальний потік
flow_value, flow_dict = nx.maximum_flow(G, "Source", "Sink", capacity='capacity')
print("Максимальний потік:", flow_value)

rows = []
for from_node, to_node, capacity in edges:
    flow = flow_dict.get(from_node, {}).get(to_node, 0)
    rows.append((from_node, to_node, capacity, flow))

df = pd.DataFrame(rows, columns=["From", "To", "Capacity", "Flow"])

# 1. Які термінали забезпечують найбільший потік товарів до магазинів?
# 2. Які маршрути мають найменшу пропускну здатність і як це впливає на загальний потік?

terminal_summary = (
    df
    .groupby("From", as_index=False)["Flow"]
    .sum()
    .sort_values(by="Flow", ascending=False)
    .head(2)
)
df['max_flow'] = df["Capacity"] - df["Flow"]
bottlenecks = df[df['max_flow'] == 0]
print("\nРебра, що є вузькими місцями (bottlenecks):")
print(bottlenecks[["From", "To", "Capacity", "Flow"]])
print("\nПотік від терміналів до магазинів:")
print(terminal_summary)

# 3. Які магазини отримали найменше товарів і чи можна збільшити їх постачання, 
# збільшивши пропускну здатність певних маршрутів?
store_summary = (
    df[df["To"].str.startswith("Store")]
    .groupby("To", as_index=False)["Flow"]
    .sum()
    .sort_values(by="Flow", ascending=True)
)
print("\nПотік до магазинів:")
print(store_summary)

"""Найменше товарів отримали Store_3, Store_9, Store_12, Store_13 та Store_14 — по 0 одиниць. Це означає, що в оптимальному розподілі максимального потоку товар до цих магазинів не був направлений.

Постачання до них можна збільшити, але для цього потрібно підвищувати пропускну здатність маршрутів, які подають товар у відповідні склади.

Для Store_3 потрібно збільшити маршрут Terminal_1 → Content_1.
Для Store_9 потрібно збільшити Terminal_1 → Content_3 або Terminal_2 → Content_3.
Для Store_12, Store_13 і Store_14 потрібно збільшити Terminal_2 → Content_4.

Причина в тому, що відповідні склади вже використали весь отриманий від терміналів потік на інші магазини."""

contents = ["Content_1", "Content_2", "Content_3", "Content_4"]
stores = [f"Store_{i}" for i in range(1, 15)]
sources = ['Terminal_1', 'Terminal_2']

terminal_store_rows = []
for content in contents:
    avaiable_from_sources = {}
    for source in sources:
        flow_to_content = flow_dict.get(source, {}).get(content, 0)
        if flow_to_content > 0:
            avaiable_from_sources[source] = flow_to_content
    for store in stores:
        flow_to_store = flow_dict.get(content, {}).get(store, 0)
        if flow_to_store > 0:
            need = flow_to_store
            for source in sources:
                available = avaiable_from_sources.get(source, 0)
                if available > 0 and need > 0:
                    sent = min(available, need)
                    terminal_store_rows.append({
                        "Terminal": source,
                        "Store": store,
                        "Flow": sent
                    })
                    avaiable_from_sources[source] -= sent
                    need -= sent

df_terminal_store = pd.DataFrame(terminal_store_rows, columns=["Terminal", "Store", "Flow"])
print("\nЗвіт з розрахунками та поясненнями :")
print("\n", df_terminal_store)