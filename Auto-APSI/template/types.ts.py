# types.ts(deprecated).py
# types.ts builder

def build(entities):
    return (
        '\n\n'.join([
            f"export type {entity.name} = {{\n"
            f"  id: string;\n"
            + '\n'.join([
                f"  {field.name}" + ("?" if not field.is_req else "") + ": "
                + ("Array<" if field.is_arr else "")
                + (field.type if not field.is_ref else (
                    f"Omit<{field.type}, " + ' | '.join([
                        f"\"{ref_field.name}\""
                        for ref_field in [
                            ref_entity for ref_entity in entities if ref_entity.name == field.type
                        ][0].fields
                        if ref_field.is_ref
                    ]) + ">"
                )) + (">" if field.is_arr else (" | null" if not field.is_req else "")) + ";"
                for field in entity.fields
            ]) + "\n"
            f"}};"
            for entity in entities
        ]) + "\n"
    )
