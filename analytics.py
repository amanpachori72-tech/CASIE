import networkx as nx

def identify_architectural_bottlenecks(G, top_n=3):
    """
    Computes betweenness centrality to isolate complex structural hubs 
    in the code dependency graph topology.
    """
    if len(G) == 0:
        return []
        
    # Programmatically calculate how often a node acts as a bridge along short paths
    centrality = nx.betweenness_centrality(G)
    
    # Sort nodes by their structural impact score
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    
    anomalies = []
    for node_name, score in sorted_nodes[:top_n]:
        node_data = G.nodes[node_name]
        anomalies.append({
            "name": node_name,
            "score": score,
            "type": node_data.get("type"),
            "line": node_data.get("line")
        })
    return anomalies