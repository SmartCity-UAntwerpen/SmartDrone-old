class Pathaction:
    object_id = 0x6048D4F4

    def __init__(self, instance, mode, end_condition, command, jump_destination=-1, error_destination=-1):
        self.instance = instance
        self.mode = mode
        self.end_condition = end_condition
        self.command = command
        self.jump_destination = jump_destination
        self.error_destination = error_destination
