"""
    Author: Charles Candelaria
    Date: 05/07/2023
    Functionality: (Abstract) Investment Class
"""

class Investment:
    """Represents an Investment"""

    investor_id = None
    """Reference owning investor"""

    def __init__(self):
        self.id = None
