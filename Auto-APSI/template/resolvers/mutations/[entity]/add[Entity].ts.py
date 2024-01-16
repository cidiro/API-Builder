# add[Entity].ts.py
# add[Entity].ts builder

def build(entity):
    return (
        # Imports
        f"import {{ {entity.name}Model, {entity.name}ModelType }} from "
        f"\"../../../db/{entity.name.lower()}/{entity.name.lower()}.ts\";\n\n"
       
        # Function header
        f"const add{entity.name} = aync (\n"
        f"  _: unknown,\n"
        f"  args: {{ "
        + ', '.join([
            f"{field.name_db}: " + (field.type if not field.is_ref else "string") + ("[]" if field.is_arr else "")
            for field in entity.fields
        ]) + " }\n"
        f"): Promise<{entity.name}ModelType> => {{\n"
             
        # Function body
        f"  const {entity.name.lower()} = new {entity.name}Model({{\n"
        + ',\n'.join([
            f"    {field.name_db}: args.{field.name_db}"
            for field in entity.fields
        ]) + "\n"
        "  });\n\n"
        
        f"  await {entity.name.lower()}.save();\n"
        f"  return {entity.name.lower()};\n"
        f"}};\n\n"
        
        f"export default add{entity.name};\n"
    )
