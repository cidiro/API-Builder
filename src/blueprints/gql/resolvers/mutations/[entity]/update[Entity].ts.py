# update[Entity].ts.py
# update[Entity].ts builder

def build(entity):
    return (
        # Imports
        f"import {{ GraphQLError }} from \"graphql\";\n"
        f"import {{ {entity.name}Model, {entity.name}ModelType }} from "
        f"\"../../../db/{entity.name.lower()}/{entity.name.lower()}.ts\";\n\n"

        # Function header
        f"const update{entity.name} = async (\n"
        f"  _: unknown,\n"
        f"  args: {{ id: string, " + ', '.join([
            f"{field.name_db}: " + (field.type if not field.is_ref else "string") + ("[]" if field.is_arr else "")
            for field in entity.fields
        ]) + " }\n"
        f"): Promise<{entity.name}ModelType> => {{\n"

        # Function body
        f"  const {entity.name.lower()} = await {entity.name}Model.findByIdAndUpdate(\n"
        f"    args.id,\n"
        f"    {{ " + ', '.join([f"{field.name_db}: args.{field.name_db}" for field in entity.fields]) + f" }},\n"
        f"    {{ new: true, runValidators: true }}\n"
        f"  ).exec();\n\n"

        f"  if (!{entity.name.lower()}) {{\n"
        f"    throw new GraphQLError(`No {entity.name.lower()} found with id ${{args.id}}`, {{\n"
        f"      extensions: {{ code: \"NOT_FOUND\" }},\n"
        f"    }});\n"
        f"  }}\n"
        f"  return {entity.name.lower()};\n"
        f"}};\n\n"

        f"export default update{entity.name};\n"
    )
