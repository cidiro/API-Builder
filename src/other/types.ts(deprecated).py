# types.ts.py
# types.ts builder

def build(entities):
    content = ""

    for entity in entities:
        content += (f"export type {entity.name} = {{\n"
                    f"  id: string;\n")

        for field in entity.fields:
            field_type = None
            if not field.is_ref:
                field_type = field.type
            else:
                omit_fields = []
                for referenced_entity in entities:
                    if referenced_entity.name == field.type:
                        omit_fields = ['"' + f.name + '"' for f in referenced_entity.fields if f.is_ref]
                        break
                if omit_fields:
                    field_type = f"Omit<{field.type}, {' | '.join(omit_fields)}>"

            if field.is_arr:
                field_type = f"Array<{field_type}>"
            else:
                if not field.is_req:
                    field_type = f"{field_type} | null"

            content += (f"  {field.name}" + ("?" if not field.is_req else "") + f": {field_type};\n")

        content += f"}};\n\n"

    return content
