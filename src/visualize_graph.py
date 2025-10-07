from agent import ERPAgent

def visualize_graph():
    """Generate and save graph visualization"""
    agent = ERPAgent()
    
    # Generate graph image
    try:
        graph_image = agent.graph.get_graph().draw_mermaid_png()
        
        # Save to file
        with open("docs/agent_graph.png", "wb") as f:
            f.write(graph_image)
        
        print("Graph visualization saved to docs/agent_graph.png")
        print("Open the file to see your agent workflow!")
        
    except Exception as e:
        print(f"Error generating graph: {e}")
        print("\nAlternative: Print graph structure")
        print(agent.graph.get_graph().to_json())

if __name__ == "__main__":
    visualize_graph()