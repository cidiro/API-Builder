# validators.ts(deprecated).py
# validators.ts builder

def build(entity, entities):
    return (
        # Imports
        f"import mongoose from \"mongoose\";\n"
        + '\n'.join([
            f"import {{ {ref_entity.name}Model }} from \"../{ref_entity.name.lower()}/{ref_entity.name.lower()}.ts\";"
            for ref_entity in entities
            if any([field.is_ref and field.type == ref_entity.name for field in entity.fields])
        ]) + "\n\n"

        # Validator functions
        + '\n\n'.join([
            f"// Validate that {field.name_db} exist" + ("s" if not field.is_arr else "") + " in the database\n"
            f"const {field.name}Exist" + ("s" if not field.is_arr else "") +
            f" = async ({field.name_db}: mongoose.Types.ObjectId" + ("[]" if field.is_arr else "") + ") => {\n"
            f"  try {{\n"
            f"    const {field.name} = await {ref_entity.name}Model"
            + (f".findById({field.name_db})" if not field.is_arr
               else f".find({{ _id: {{ $in: {field.name_db} }} }})") + ";\n"
            f"    return "
            + (f"!!{field.name}" if not field.is_arr else f"{field.name}.length === {field.name_db}.length") + ";\n"
            f"  }} catch (_e) {{\n"
            f"    return false;\n"
            f"  }}\n"
            f"}};"
            for ref_entity in entities
            for field in entity.fields
            if field.is_ref and field.type == ref_entity.name
        ]) + "\n\n"

        # Export validators
        f"export const validators = {{\n"
        + ',\n'.join([
            f"  {field.name}Exist" + ("s" if not field.is_arr else "")
            for field in entity.fields
            if field.is_ref
        ]) + "\n"
        f"}};\n"
    )
