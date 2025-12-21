import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import ERPAgent
from langchain_core.messages import HumanMessage

def main():
    print("="*60)
    print("ERP Implementation Assistant")
    print("="*60)
    
    try:
        agent = ERPAgent()
        print("✅ Agent loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading agent: {e}")
        return
    
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
            
            # Display sources
            sources = agent.get_last_sources()
            if sources:
                print(f"\n📚 Sources ({len(sources)} documents):")
                for i, source in enumerate(sources, 1):
                    module_info = f" (Module: {source['module']})" if source['module'] != 'Unknown' else ""
                    doc_type_info = f" [Type: {source['doc_type']}]" if source['doc_type'] != 'Unknown' else ""
                    print(f"  {i}. {source['source']}{module_info}{doc_type_info}")
            
            conversation_history = updated_history
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()