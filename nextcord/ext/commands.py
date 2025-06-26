class Bot:
    def __init__(self, command_prefix=None, intents=None):
        self.command_prefix = command_prefix
        self.intents = intents
        self._events = {}
        self.tree = self

    def run(self, token):
        print(f"[RUNNING BOT] token={token[:6]}...")

    def command(self, name=None):
        def decorator(func):
            return func
        return decorator

    def event(self, func):
        self._events[func.__name__] = func
        return func

    def slash_command(self, name=None, description=None):
        def decorator(func):
            return func
        return decorator