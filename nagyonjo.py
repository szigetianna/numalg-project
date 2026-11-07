import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

# --- BEÁLLÍTÁSOK ---
nodes = 500
n_traits = 8
st_c_p = (1/nodes) * 3 
alpha = 2
decay = 0.995
threshold = 1e-4
num_events = 100
random_meet_p = 0.1
lvls_of_t = 2
amount = 1.5

traits = np.random.randint(0, lvls_of_t, size=(nodes, n_traits))
link = [[] for _ in range(nodes)]
weight = [[] for _ in range(nodes)]

# --- SEGÉDFÜGGVÉNYEK ---

def similarity(i, j):
    return np.mean(traits[i] == traits[j])

def create_initial_links():
    print("--- 1. KEZDETI LÉPÉS: Kapcsolatok generálása... ---")
    for i in range(nodes):
        for j in range(i+1, nodes):
            sim = similarity(i, j)
            p = st_c_p * (1 + alpha * sim)
            if random.random() < p:
                w = random.uniform(0.5, 1.5)
                link[i].append(j); weight[i].append(w)
                link[j].append(i); weight[j].append(w)
    print(f"   -> Kezdeti kapcsolatok létrehozva.\n")

def add_or_strengthen(a, b):
    if b in link[a]:
        idx = link[a].index(b)
        weight[a][idx] += amount
        idx = link[b].index(a)
        weight[b][idx] += amount
    else:
        sim = similarity(a, b)
        p = st_c_p * (1 + alpha * sim)
        if random.random() < p:
            w = random.uniform(0.5, 1.5)
            link[a].append(b); weight[a].append(w)
            link[b].append(a); weight[b].append(w)

def new_sim_con():
    if random.random() < random_meet_p:
        i = random.randint(0, nodes-1)
        sims = np.array([similarity(i, j) for j in range(nodes)], dtype=float)
        sims[i] = 0
        sims = sims ** alpha 
        if sims.sum() > 0:
            j = np.random.choice(range(nodes), p=sims / sims.sum())
            add_or_strengthen(i, j)

def triadikus():
    i = random.randint(0, nodes-1)
    if not link[i]: return
    
    w_i = np.array(weight[i], dtype=float)
    sim_i = np.array([similarity(i, x) for x in link[i]], dtype=float)
    combined_i = w_i * (1 + alpha * sim_i)
    if combined_i.sum() == 0: return
    
    j = np.random.choice(link[i], p=combined_i / combined_i.sum())
    if not link[j]: return

    js = link[j]
    w_j = np.array([weight[j][link[j].index(x)] for x in js], dtype=float)
    sim_j = np.array([similarity(j, x) for x in js], dtype=float)
    combined_j = w_j * (1 + alpha * sim_j)
    if combined_j.sum() == 0: return

    k = np.random.choice(js, p=combined_j / combined_j.sum())
    if k == i: return

    add_or_strengthen(i, j)
    add_or_strengthen(j, k)
    add_or_strengthen(i, k)
    
def gyengules_torles():
    edges_to_delete = set()
    for a in range(nodes):
        for idx, b in enumerate(link[a]):
            new_w = weight[a][idx] * decay
            if new_w < threshold:
                edges_to_delete.add(tuple(sorted((a, b))))
            weight[a][idx] = new_w
            
    for (u, v) in edges_to_delete:
        if v in link[u]:
            idx = link[u].index(v); del link[u][idx]; del weight[u][idx]
        if u in link[v]:
            idx = link[v].index(u); del link[v][idx]; del weight[v][idx]
            
def events():
    print(f"--- 2. SZIMULÁCIÓ: {num_events} esemény futtatása... ---")
    for event in np.arange(1, num_events+1):
        new_sim_con()
        triadikus()
        gyengules_torles()
    print("   -> Szimuláció kész.\n")

# --- KIRAJZOLÁS ---

def kirajzolas():
    print("--- 3. KIRAJZOLÁS ---")

    # 1. Gráf építése
    G = nx.Graph()
    for i in range(nodes):
        for idx, j in enumerate(link[i]):
            if i < j:
                G.add_edge(i, j, weight=weight[i][idx])

    if G.number_of_edges() == 0:
        print("Üres gráf.")
        return

    # 2. Központi ember kiválasztása
    degrees = dict(G.degree(weight='weight'))
    fokusz_ember = max(degrees, key=degrees.get)
    print(f"Középpontban: {fokusz_ember} (Súlyozott fokszám: {degrees[fokusz_ember]:.2f})")

    # 3. Részgráf (Ego network)
    subG = nx.ego_graph(G, fokusz_ember, radius=2)
    
    # 4. Geocentrikus elrendezés
    # Rögzítjük a fókusz embert középre (0,0), a többieket hagyjuk rendeződni
    pos = nx.spring_layout(subG, 
                           pos={fokusz_ember: (0, 0)}, # Kezdő pozíció a központnak
                           fixed=[fokusz_ember],       # "Leszögezzük" a központot
                           k=0.6,                      # Távolság (nagyobb = szellősebb)
                           iterations=100,             # Több iteráció a szebb rendeződésért
                           seed=42)

    # 5. Stílus beállítások
    node_strengths = [subG.degree(n, weight='weight') for n in subG.nodes()]
    
    # Méretezés finomhangolása
    min_s, max_s = min(node_strengths), max(node_strengths)
    if max_s == min_s: max_s += 1
    node_sizes = [200 + (s - min_s) / (max_s - min_s) * 800 for s in node_strengths]

    # Élek vastagsága
    weights = [subG[u][v]['weight'] for u, v in subG.edges()]
    if weights:
        w_min, w_max = min(weights), max(weights)
        edge_widths = [0.5 + (w - w_min)/(w_max - w_min)*2.5 if w_max > w_min else 1.0 for w in weights]
    else:
        edge_widths = []

    # 6. Kirajzolás
    plt.figure(figsize=(12, 12)) 
    ax = plt.gca()
    
    # Élek rajzolása
    nx.draw_networkx_edges(subG, pos, width=edge_widths, alpha=0.2, edge_color='#555555')

    # A többi ember rajzolása
    # Nodelist szűrése (mindenki, aki nem a fókusz ember)
    others = [n for n in subG.nodes() if n != fokusz_ember]
    other_sizes = [node_sizes[list(subG.nodes()).index(n)] for n in others]
    other_colors = [node_strengths[list(subG.nodes()).index(n)] for n in others]

    nx.draw_networkx_nodes(subG, pos, 
                           nodelist=others,
                           node_size=other_sizes, 
                           node_color=other_colors, 
                           cmap=plt.cm.viridis,
                           alpha=0.85,
                           edgecolors='white')

    # A központi ember rajzolása (kiemelve)
    nx.draw_networkx_nodes(subG, pos, 
                           nodelist=[fokusz_ember], 
                           node_size=node_sizes[list(subG.nodes()).index(fokusz_ember)] * 1.3, 
                           node_color='#FF4500', 
                           edgecolors='black', 
                           linewidths=2)

    # Címkék
    # Csak a központi ember és a közvetlen szomszédok kapjanak címkét, hogy ne legyen zsúfolt
    labels = {}
    neighbors = list(G.neighbors(fokusz_ember))
    labels[fokusz_ember] = str(fokusz_ember)
    for n in neighbors:
        if n in subG.nodes():
            labels[n] = str(n)
            
    nx.draw_networkx_labels(subG, pos, labels=labels, font_size=8, font_weight='bold')

    plt.title(f"{fokusz_ember}. ember kapcsolati hálója (Központosított nézet)", fontsize=15)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# --- FUTTATÁS ---
create_initial_links()
events()
kirajzolas()