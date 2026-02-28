from memory.persistent import init_db, set_memory, get_memory


class ContextMemory:

    def __init__(self):

        init_db()

        self.last_path = get_memory("last_path")
        self.last_action = get_memory("last_action")

    def update(self, *, path=None, action=None):

        if path:
            self.last_path = path
            set_memory("last_path", path)

        if action:
            self.last_action = action
            set_memory("last_action", action)

    def resolve_pronoun(self, text: str):

        pronouns = ("it", "this", "that")

        words = text.lower().split()

        if any(p in words for p in pronouns):
            return self.last_path

        return None


context = ContextMemory()