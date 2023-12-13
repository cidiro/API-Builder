import re
from Entity import *


# entity_parser parses a file containing entities in TypeScript
# and returns a list of all the entities found in the file
def entity_parser(filepath):
    # entities is a list of type Entity
    entities = []

    # Open the file
    with open(filepath, "r") as file:
        # Read the file
        lines = file.readlines()

        # Iterate through each line
        for index, line in enumerate(lines):
            # If the line is the start of an entity
            if line.startswith("export type"):
                # Get the name of the entity
                entity_name = line.split()[2]

                # Create a new entity
                entity = Entity(entity_name)

                # Iterate through the lines after the entity name
                for entity_line in lines[index + 1:]:
                    # If the line is the end of the entity
                    if entity_line.startswith("};"):
                        # Add the entity to the list of entities
                        entities.append(entity)
                        break

                    if re.match(r".+: .+;", entity_line):
                        # Get the field name and type
                        field_name = entity_line.split(":")[0].strip(" ?")
                        if field_name != "id":
                            field_type = entity_line.split(":")[1].strip().split(";")[0]
                            field_type = field_type.split("<")[-1].split(">")[0].split(",")[0]

                            # Create a new field
                            field = Field(
                                field_name,
                                field_type,
                                is_array="Array<" in entity_line,
                                required=entity_line.split(":")[0].strip()[-1] != "?"
                            )

                            # Add the field to the entity
                            entity.add_field(field)

    # Check every field in every entity
    # If the field type is an entity name, set is_ref to True
    for entity in entities:
        for field in entity.fields:
            for other_entity in entities:
                if field.type == other_entity.name:
                    field.is_ref = True
                    field.alt_name = other_entity.name.lower() + "ID" + ("s" if field.is_array else "")
                    field.alt_type = "string" + ("[]" if field.is_array else "")
                    break

    return entities
