import inspect


def get_class_property_names(self: object) -> list[str]:
    class_property_names = []
    for name, value in inspect.getmembers(self.__class__):
        if isinstance(value, property):
            class_property_names.append(name)
    return class_property_names
