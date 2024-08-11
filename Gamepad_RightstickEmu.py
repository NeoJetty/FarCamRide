import signal
import sys
import threading
import keyboard
import vgamepad as vg
from console_output import print_stick_states
from left_stick import LeftStick
from right_stick import RightStick

# Define scan codes for the keys
SCAN_CODES = {
    'num_8': 72,
    'num_4': 75,
    'num_6': 77,
    'num_2': 80,
    'num_5': 76,
    'num_plus': 78,
    'num_minus': 74,
    'num_7': 71,  # Rotates clockwise
    'num_9': 73,  # Rotates counterclockwise
}

# Create a single virtual Xbox 360 controller instance
virtual_controller = vg.VX360Gamepad()

# Create instances of the LeftStick and RightStick with the same controller
left_stick = LeftStick(virtual_controller)
right_stick = RightStick(virtual_controller)

def handle_key_event(event):
    """Handle key release events only for specific numpad keys."""
    global left_stick, right_stick

    if event.event_type == 'up':
        if event.scan_code == SCAN_CODES['num_5']:  # Reset right stick
            right_stick.reset()

        elif event.scan_code in [SCAN_CODES['num_8'], SCAN_CODES['num_4'], SCAN_CODES['num_6'], SCAN_CODES['num_2']]:  # Right stick controls
            direction_x, direction_y = 0.0, 0.0
            if event.scan_code == SCAN_CODES['num_8']:
                direction_y = 1
            elif event.scan_code == SCAN_CODES['num_4']:
                direction_x = -1
            elif event.scan_code == SCAN_CODES['num_6']:
                direction_x = 1
            elif event.scan_code == SCAN_CODES['num_2']:
                direction_y = -1

            right_stick.move(direction_x, direction_y)

        if event.scan_code == SCAN_CODES['num_plus']:  # Increase state (e.g., move to next state)
            left_stick.change_state(1)  # Move to the next state in the list

        elif event.scan_code == SCAN_CODES['num_minus']:  # Decrease state (e.g., move to previous state)
            left_stick.change_state(-1)  # Move to the previous state in the list

        elif event.scan_code == SCAN_CODES['num_7']:  # Rotate left stick clockwise
            left_stick.rotate_counterclockwise()

        elif event.scan_code == SCAN_CODES['num_9']:  # Rotate left stick counterclockwise
            left_stick.rotate_clockwise()

def signal_handler(sig, frame):
    """Handle SIGINT signal (Ctrl+C)."""
    print('Exiting...')
    sys.exit(0)

def main():
    # Set up the signal handler for interrupts
    signal.signal(signal.SIGINT, signal_handler)

    # Start the periodic printing of stick states
    threading.Thread(target=print_stick_states, args=(left_stick, right_stick), daemon=True).start()

    # Set up the keyboard listener for key events
    keyboard.hook(handle_key_event)
    
    # Keep the script running
    print("Listening for numpad key releases (2, 4, 5, 6, 7, 8, 9, +, -). Press Ctrl+C to exit.")
    keyboard.wait('esc')  # Wait indefinitely until 'esc' is pressed

if __name__ == "__main__":
    main()
