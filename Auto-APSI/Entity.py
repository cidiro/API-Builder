# Entity.py

class Field:
    def __init__(self):
        self.name = None
        self.name_db = None
        self.type = None
        self.type_gql = None
        self.is_arr = None
        self.is_req = None
        self.is_ref = False
        self.is_unique = False

    def __str__(self):
        return (f"{self.name}: {self.type} (db: {self.name_db}, gql: {self.type_gql}, arr: {self.is_arr}, "
                f"req: {self.is_req}, ref: {self.is_ref}, unique: {self.is_unique})")


class Entity:
    def __init__(self):
        self.name = None
        self.name_plural = None
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)

    def __str__(self):
        return f"{self.name} / {self.name_plural}\n" + "\n".join([str(field) for field in self.fields]) + "\n"

    __repr__ = __str__
