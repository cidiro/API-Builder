# [Entity].ts.py
# [Entity].ts builder

def build(entity):
    return (
        # Imports
        f"import {{ {entity.name}ModelType }} from \"../../db/{entity.name.lower()}/{entity.name.lower()}.ts\";\n"
        + '\n'.join([
            f"import {{ {ref_field.type}Model, {ref_field.type}ModelType }} "
            f"from \"../../db/{ref_field.type.lower()}/{ref_field.type.lower()}.ts\";"
            for ref_field in entity.fields
            if ref_field.is_ref
        ]) + "\n\n"

        # Reference resolvers
        f"export const {entity.name} = {{\n"
        + ',\n'.join(
            # Referenced Non-Array Fields
            [
                f"  {ref_field.name}: async (parent: {entity.name}ModelType): Promise<{ref_field.type}ModelType | null> => {{\n"
                f"    const {ref_field.name} = await {ref_field.type}Model.findOne({{ _id: parent.{ref_field.name_db} }});\n"
                f"    return {ref_field.name} || null;\n"
                f"  }}"
                for ref_field in entity.fields
                if ref_field.is_ref and not ref_field.is_arr
            ]
            # Referenced Array Fields
            + [
                f"  {ref_field.name}: async (parent: {entity.name}ModelType): Promise<{ref_field.type}ModelType[]> => {{\n"
                f"    const {ref_field.name} = await {ref_field.type}Model.find({{ _id: {{ $in: parent.{ref_field.name_db} }} }});\n"
                f"    return {ref_field.name};\n"
                f"  }}"
                for ref_field in entity.fields
                if ref_field.is_ref and ref_field.is_arr
            ]
        ) + "\n"
        f"}};\n"
    )
