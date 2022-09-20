class Action():
    def __init__(self, delay: int, steps: int):
        self.delay = delay
        self.steps = steps

    def dictionary(self):
        return {
            "delay": self.delay,
            "steps": self.steps,
        }
