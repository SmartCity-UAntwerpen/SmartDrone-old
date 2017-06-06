class Pathaction:
    object_id = 0x6048D4F4

    def __init__(self, instance, mode, end_condition, command, mode_parameters=[0.0, 0.0, 0.0, 0.0],
                 condition_parameters=[0.0, 0.0, 0.0, 0.0], jump_destination=-1, error_destination=-1):
        self.instance = instance
        self.mode = mode
        self.end_condition = end_condition
        self.command = command
        self.jump_destination = jump_destination
        self.error_destination = error_destination
        self.mode_parameters = mode_parameters
        self.condition_parameters = condition_parameters
