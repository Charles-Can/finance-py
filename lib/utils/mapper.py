"""
    Author: Charles Candelaria
    Date: 05/07/2023
    Functionality:  Mapper class maps list indexes to a class Object. 
                    Supports chainable calls
"""


class PropertyMapper:
    """Maps list indexes to a class properties"""

    def __init__(self):
        self.__mappings = {}
        """Holds index to prop mappings"""

    def add_mapping(self, from_key, to_key):
        """Adds mapping, chainable"""
        self.__mappings[from_key] = to_key
        return self

    def map_properties(self, from_list, to_obj):
        """Maps list to object"""
        for from_prop in self.__mappings:
            # iterate mappings
            to_prop = self.__mappings[from_prop]
            # grab destination property
            setattr(to_obj, to_prop, from_list[from_prop])
            # dynamically set property on object from list index
