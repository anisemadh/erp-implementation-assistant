from agent import ERPAgent
from langchain_core.messages import HumanMessage

def main():
    print("="*60)
    print("ERP Implementation Assistant")
    print("="*60)
    
    agent = ERPAgent()
    conversation_history = []
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            print("\nAssistant: ", end="", flush=True)
            response, updated_history = agent.run(user_input, conversation_history)
            print(response)
            conversation_history = updated_history
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()