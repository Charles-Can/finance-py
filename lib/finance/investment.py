from uuid import uuid1

class Investment:

    investor_id = None
    """Reference owning investor"""

    def __init__(self):
        self.id = uuid1()
