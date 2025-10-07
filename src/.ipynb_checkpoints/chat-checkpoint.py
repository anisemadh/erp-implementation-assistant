from agent import ERPAgent
from langchain_core.messages import HumanMessage

def main():
    print("="*60)
    print("ERP Implementation Assistant")
    print("Ask questions about Infor ERP configuration and implementation")
    print("Type 'exit' or 'quit' to end the conversation")
    print("="*60)
    
    agent = ERPAgent()
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        # Get response from agent
        try:
            print("\nAssistant: ", end="", flush=True)
            response = agent.run(user_input)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again with a different question.")

if __name__ == "__main__":
    main()