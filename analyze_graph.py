import json

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

nodes_df = pd.read_csv("quaker-nodes.csv")
edges_df = pd.read_csv("quaker-edges.csv")

G = nx.Graph()

for _, row in nodes_df.iterrows():
    G.add_node(row["Id"], label=row["Label"], gender=row["gender"])

for _, row in edges_df.iterrows():
    G.add_edge(row["Source"], row["Target"])

print("🔹 Вузлів:", G.number_of_nodes())
print("🔹 Зв'язків:", G.number_of_edges())
print("🔹 Щільність графа:", round(nx.density(G), 4))
print("🔹 Середній ступінь вузла:", round(sum(dict(G.degree()).values()) / G.number_of_nodes(), 2))

degree_centrality = nx.degree_centrality(G)
top_5 = sorted(degree_centrality.items(), key=lambda x: -x[1])[:5]
print("\n🔝 ТОП-5 користувачів за degree centrality:")
for user_id, centrality in top_5:
    name = G.nodes[user_id]['label']
    print(f"{name} ({user_id}): {round(centrality, 3)}")

clusters = list(nx.connected_components(G))
print("\n🔗 Кількість кластерів:", len(clusters))
print("📌 Розмір найбільшого кластеру:", max(len(c) for c in clusters))

plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=False, node_size=50, alpha=0.7)
nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]['label'] for n in G.nodes if degree_centrality[n] > 0.1}, font_size=8)
plt.title("Граф соціальної мережі (Quakers)")
plt.show()


export_data = {
    "nodes": [{"id": n, "label": G.nodes[n]["label"], "gender": G.nodes[n]["gender"]} for n in G.nodes],
    "edges": [{"source": u, "target": v} for u, v in G.edges]
}
with open("graph_export.json", "w", encoding="utf-8") as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)
print("✅ Експорт у graph_export.json завершено.")
