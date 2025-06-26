class Bot:
    def __init__(self, **kwargs): pass

def slash_command(name=None, description=None):
    def wrapper(func): return func
    return wrapper