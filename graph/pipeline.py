from langgraph.graph import StateGraph, END
from graph.state import AdState
from agents.agent1_vision import agent1_analyze
from agents.agent2_image_gen import agent2_generate

def build_graph():
    graph = StateGraph(AdState)

    # Ajouter les noeuds
    graph.add_node("agent1_vision", agent1_analyze)
    graph.add_node("agent2_image_gen", agent2_generate)

    # Définir le flux
    graph.set_entry_point("agent1_vision")
    graph.add_edge("agent1_vision", "agent2_image_gen")
    graph.add_edge("agent2_image_gen", END)

    return graph.compile()

# Instance globale réutilisable
ad_pipeline = build_graph()