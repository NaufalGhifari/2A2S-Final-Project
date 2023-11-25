"""
    # main.py 
    main file of the project
"""

from app import run_gui

def startMessage():
    print("\n+========================================+")
    print("| 2A2S: AI Augmented Surveillance System |")
    print("+========================================+\n")
    print("Loading, please wait...")

def main():
    run_gui()

if (__name__ == "__main__"):
    startMessage()
    main()