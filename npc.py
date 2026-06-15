class NPC:
    def __init__(self, name, x, y, predictability):
        self.name = name
        self.x = x
        self.y = y
        self.predictability = predictability
        self.last_seen = None
        self.behavior_signature = "A"
