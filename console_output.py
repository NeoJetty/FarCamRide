import os
import time
import math
from utils import adjust_value

def clear_terminal():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_stick_states(left_stick, right_stick):
    """Print the current state of both sticks every 0.2 seconds."""
    while True:
        clear_terminal()
        left_x = left_stick.get_x()
        left_y = left_stick.get_y()
    
        print(f"Left Stick -> ({left_x:.2f}, {left_y:.2f}) | Amplitude: {left_stick.amplitude}, Rotation: {left_stick.rotation}°")
        print(f"Right Stick -> ({right_stick.position['x']:.2f}, {right_stick.position['y']:.2f})")
        time.sleep(0.2)
