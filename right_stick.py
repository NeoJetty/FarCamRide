from utils import adjust_value

class RightStick:
    def __init__(self, virtual_controller):
        self.virtual_controller = virtual_controller
        self.position = {'x': 0.0, 'y': 0.0}

    def apply_deadzone(self, value):
        """Apply deadzone logic."""
        if abs(value) < 0.205:  # Assuming 0.205 is the deadzone threshold
            return 0.0
        return value

    def move(self, direction_x, direction_y):
        if direction_x != 0:  # Horizontal movement
            if self.position['x'] == 0.0:
                self.position['x'] = 0.205 * direction_x # move from 0 to 0.2 to skip deadzone
            else:
                self.position['x'] += 0.005 * direction_x
            self.position['x'] = self.apply_deadzone(self.position['x'])

        if direction_y != 0:  # Vertical movement
            if self.position['y'] == 0.0:
                self.position['y'] = 0.205 * direction_y # move from 0 to 0.2 to skip deadzone
            else:
                self.position['y'] += 0.005 * direction_y
            self.position['y'] = self.apply_deadzone(self.position['y'])

        # Apply deadzone logic once and then clamp
        self.position['x'] = max(-1.0, min(1.0, self.position['x']))
        self.position['y'] = max(-1.0, min(1.0, self.position['y']))

        self.update()

    def update(self):
        self.virtual_controller.right_joystick_float(self.position['x'], self.position['y'])
        self.virtual_controller.update()

    def reset(self):
        """Reset the right stick position."""
        self.position = {'x': 0.0, 'y': 0.0}
        self.update()
