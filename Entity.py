class Field:
    def __init__(self, name, type, is_array=False, required=True, is_ref=False, alt_name=None, alt_type=None):
        self.name = name
        self.type = type
        self.is_array = is_array
        self.required = required
        self.is_ref = is_ref
        self.alt_name = alt_name
        self.alt_type = alt_type

    def __str__(self):
        return f"{self.name}: {self.type}"


class Entity:
    def __init__(self, name, fields=None):
        self.name = name
        self.fields = [] if fields is None else fields

    def add_field(self, field):
        self.fields.append(field)

    def __str__(self):
        return f"{self.name}\n" + "\n".join([str(field) for field in self.fields]) + "\n"

    __repr__ = __str__
