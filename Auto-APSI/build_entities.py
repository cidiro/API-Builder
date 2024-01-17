# build_entities.py

import sys
import json
from Entity import *


def build_entities(json_filepath):
    with open(json_filepath, 'r') as file:
        entities_json = json.load(file)

    entities = []
    for entity_json in entities_json:
        entity = Entity()
        entity.name = entity_json["name"]
        entity.name_plural = entity_json["name_plural"]

        for field_json in entity_json["fields"]:
            field = Field()
            field.name = field.name_db = field_json["name"]
            field.type = "number" if field_json["type"] in ["int", "float"] else field_json["type"]
            field.type_gql = field_json["type"].capitalize()
            field.is_arr = field_json["is_array"]
            field.is_req = field_json["is_required"]
            field.is_unique = field_json["is_unique"]
            entity.add_field(field)

        entities.append(entity)

    for entity in entities:
        for field in entity.fields:
            for other_entity in entities:
                if field.type == other_entity.name:
                    field.is_ref = True
                    field.name_db = other_entity.name.lower() + "ID" + ("s" if field.is_arr else "")

    return entities
