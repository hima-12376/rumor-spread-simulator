import networkx as nx
import random

def simulate_spread(amp_score, validity):

    # Create random social network
    G = nx.erdos_renyi_graph(300, 0.02)

    # Initialize all as Susceptible
    for node in G.nodes():
        G.nodes[node]['state'] = 'S'

    # Random initial infected node
    infected = random.choice(list(G.nodes()))
    G.nodes[infected]['state'] = 'I'

    # Spread probability influenced by:
    # Emotional intensity AND public belief
    spread_prob = (0.1 + amp_score) * validity

    # Simulate 5 time steps
    for _ in range(5):
        new_infected = []

        for node in G.nodes():
            if G.nodes[node]['state'] == 'I':
                for neigh in G.neighbors(node):
                    if G.nodes[neigh]['state'] == 'S':
                        if random.random() < spread_prob:
                            new_infected.append(neigh)

        for ni in new_infected:
            G.nodes[ni]['state'] = 'I'

    return G