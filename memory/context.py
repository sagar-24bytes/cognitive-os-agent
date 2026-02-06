# memory/context.py

class ContextMemory:
    def __init__(self):
        self.last_path = None
        self.last_action = None

    def update(self, *, path=None, action=None):
        if path:
            self.last_path = path
        if action:
            self.last_action = action

    def resolve_pronoun(self, text: str):
        """
        Resolve 'it / this / that' to last known path
        """
        pronouns = ("it", "this", "that")
        words = text.lower().split()

        if any(p in words for p in pronouns):
            return self.last_path

        return None


# singleton context (important)
context = ContextMemory()
