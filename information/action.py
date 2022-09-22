class Action():
    def __init__(self, delay: int, steps: int):
        self.delay = delay
        self.steps = steps
        self.start_at = 0

    def dictionary(self):
        return {
            "delay": self.delay,
            "steps": self.steps,
            "start_at": self.start_at
        }
