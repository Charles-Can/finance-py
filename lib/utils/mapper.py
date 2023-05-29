"""
    Author: Charles Candelaria
    Date: 05/07/2023
    Functionality:  Mapper class maps list indexes to a class Object. 
                    Supports chainable calls

    Author: Charles Candelaria
    Updated: 05/29/2023
    Notes: Extends mapper options to take functions as well as str and int
"""
from typing import Callable, Any, Self


class PropertyMapper:
    """Maps list indexes to a class properties"""

    def __init__(self):
        self.__mappings: list[tuple[Callable[[Any], Any] | int |
                                    str, Callable[[Any, Any], None] | int | str]] = []
        """Holds index to prop mappings"""

    def __read_prop(self, reader: Callable[[Any], Any] | str | int, source: Any) -> Any:
        """Reads property value from source object"""
        source_value = None

        match reader:
            case str() | int():
                # If string int treat source read as a dumb prop match
                source_value = source[reader]
            case _:
                # reader is a function to be called passing the source
                source_value = reader(source)

        return source_value

    def __write_prop(self, writer: Callable[[Any, Any], None] | str | int, value: Any, dest: Any):
        """Write value to source"""
        match writer:
            case str() | int():
                # writer is str or int treat a simple assignment
                # dynamically set property on object from list index
                setattr(dest, writer, value)
            case _:
                # writer is a function to be called with dest and value
                writer(dest, value)

    def add_mapping(self, source: int | str | Callable[[Any], Any], dest: str | Callable[[Any, Any], None]) -> Self:
        """Adds mapping, chainable"""
        self.__mappings.append((source, dest))
        return self

    def map_properties(self, source: list | tuple | dict, dest: Any):
        """Maps list to object"""

        for mapper in self.__mappings:
            reader, writer = mapper  # get reader and writer
            source_value = self.__read_prop(reader, source)  # read value
            self.__write_prop(writer, source_value, dest)  # write value
