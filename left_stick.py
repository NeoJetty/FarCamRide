import math

class LeftStick:
    # Deadzone values for different states
    DEADZONES = {
        'stand': 0,
        'walk': 17,
        'run': 12
    }
    # Amplitude values for different states
    AMPLITUDES = {
        'stand': 0.0,
        'walk': 0.7,
        'run': 1.0
    }

    def __init__(self, virtual_controller):
        self.virtual_controller = virtual_controller
        self.rotation = 270  # Default rotation pointing upwards
        self.states = ['stand', 'walk', 'run']
        self.current_state_index = 0  # Start in 'stand' state
        self.amplitude = self.get_amplitude_for_state()
        self.update()

    def get_amplitude_for_state(self):
        """Return amplitude based on the current state."""
        state = self.states[self.current_state_index]
        return self.AMPLITUDES[state]

    def set_state(self, state_name):
        """Set the state and adjust amplitude accordingly."""
        if state_name in self.states:
            self.current_state_index = self.states.index(state_name)
            self.amplitude = self.get_amplitude_for_state()
            self.update()

    def rotate_clockwise(self):
        self.rotation = (self.rotation + 3) % 360  # Decrease rotation for clockwise
        self.rotation = self.correct_deadzone_clockwise(self.rotation)
        self.update()

    def rotate_counterclockwise(self):
        self.rotation = (self.rotation - 3) % 360  # Increase rotation for counterclockwise
        self.rotation = self.correct_deadzone_counterclockwise(self.rotation)
        self.update()

    def get_current_deadzone(self):
        """Return the deadzone for the current state."""
        state = self.states[self.current_state_index]
        return self.DEADZONES[state]

    def correct_deadzone_clockwise(self, rotation):
        """Adjust rotation to avoid deadzone values."""

        dz = self.get_current_deadzone()
        if dz == 0:
            return rotation  # No correction needed for zero deadzone

        # Jumping out of neutral state to first non-deadzone value
        if dz > rotation >= 0:
            return dz
        elif 90+dz > rotation >= 90:
            return 90+dz
        elif 180+dz > rotation >= 180:
            return 180+dz
        elif 270+dz > rotation >= 270:
            return 270+dz
        
        # Jumping into neutral state if entering deadzone
        if 360-dz < rotation < 360:
            return 0
        elif 90-dz < rotation < 90:
            return 90  
        elif 180-dz < rotation < 180:
            return 180  
        elif 270-dz < rotation < 270:
            return 270 
        
        # Do nothing if rotation is in non-deadzone area
        return rotation

    def correct_deadzone_counterclockwise(self, rotation):
        """Adjust rotation to avoid deadzone values."""
        dz = self.get_current_deadzone()
        if dz == 0:
            return rotation  # No correction needed for zero deadzone

        # Jumping out of neutral state to first non-deadzone value
        if 360-dz < rotation < 360:
            return 360-dz   
        elif 90-dz < rotation <= 90:
            return 90-dz
        elif 180-dz < rotation <= 180:
            return 180-dz
        elif 270-dz < rotation <= 270:
            return 270-dz

        # Jumping into neutral state if entering deadzone
        if 0 < rotation < dz:
            return 0
        elif 90 < rotation < 90 + dz:
            return 90  
        elif 180 < rotation < 180 + dz:
            return 180  
        elif 270 < rotation < 270 + dz:
            return 270 
        
        # Do nothing if rotation is in non-deadzone area
        return rotation

    def change_state(self, direction):
        """Change the movement state based on direction (1 for faster, -1 for slower)."""
        self.current_state_index = max(0, min(self.current_state_index + direction, len(self.states) - 1))
        self.amplitude = self.get_amplitude_for_state()
        self.update()

    def update(self):
        self.x = self.amplitude * math.cos(math.radians(-self.rotation))
        self.y = self.amplitude * math.sin(math.radians(-self.rotation))
        self.virtual_controller.left_joystick_float(self.x, self.y)
        self.virtual_controller.update()

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y