def adjust_value(value, deadzone=0.205):
    """Adjust value based on the deadzone."""
    if abs(value) < deadzone:
        return 0.0
    if value > 0:
        return value + 0.21
    elif value < 0:
        return value - 0.21
    return value
