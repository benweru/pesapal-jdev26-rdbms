import sys
from parser import parse_command
import json

def repl():
    print("BenDB: Simple RDBMS (v0.1)")
    print("Type 'EXIT' to quit.")
    
    while True:
        try:
            command = input("bendb> ").strip()
            if not command:
                continue
                
            if command.upper() == "EXIT":
                break
                
            result = parse_command(command)
            
            # Pretty print the result
            if isinstance(result, list):
                print(json.dumps(result, indent=2))
            else:
                print(result)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()