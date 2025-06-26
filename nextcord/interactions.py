class Interaction:
    def __init__(self, user=None):
        self.user = user

class SlashOption:
    def __init__(self, name=None, description=None, required=False):
        self.name = name
        self.description = description
        self.required = required