import sys

def repl():
    print("BenDB: Simple RDBMS (v0.1)")
    print("Type 'EXIT' to quit.")
    
    while True:
        try:
            command = input("bendb> ").strip()
            if command.upper() == "EXIT":
                break
            print(f"Unrecognized command: {command}")
            # TODO: Pass command to parser
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    repl()