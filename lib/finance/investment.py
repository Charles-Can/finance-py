"""
    Author: Charles Candelaria
    Date: 05/07/2023
    Functionality: (Abstract) Investment Class
"""
from uuid import uuid1


class Investment:
    """Represents an Investment"""

    investor_id = None
    """Reference owning investor"""

    def __init__(self):
        self.id = uuid1()
