class CSVPropertyMapper:
    def __init__(self):
        self.__mappings = {}

    def add_mapping(self, from_key, to_key):
        self.__mappings[from_key] = to_key
        return self

    def map_properties(self, from_list, to_obj):
        for from_prop in self.__mappings:
            to_prop = self.__mappings[from_prop]
            setattr(to_obj, to_prop, from_list[from_prop])