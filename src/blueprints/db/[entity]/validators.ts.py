# validators.ts.py
# validators.ts builder

def build(entity):
    return (
        # Imports
        f"import mongoose from \"mongoose\";\n"
        + '\n'.join([
            f"import {{ {ref_field.type}Model }} from \"../{ref_field.type.lower()}/{ref_field.type.lower()}.ts\";"
            for ref_field in entity.fields
            if ref_field.is_ref
        ]) + "\n\n"
            
        # Validator functions
        + '\n\n'.join([
            # Reference Non-Array Fields
            (
                f"// Validate that {ref_field.name_db} exists in the database\n"
                f"const {ref_field.name}Exists = async ({ref_field.name_db}: mongoose.Types.ObjectId) => {{\n"
                f"  try {{\n"
                f"    const {ref_field.name} = await {ref_field.type}Model.findById({ref_field.name_db});\n"
                f"    return !!{ref_field.name};\n"
                f"  }} catch (_e) {{\n"
                f"    return false;\n"
                f"  }}\n"
                f"}};"
            ) if ref_field.is_ref and not ref_field.is_arr else ""

            # Reference Array Fields
            + (
                f"// Validate that all {ref_field.name_db} exist in the database\n"
                f"const {ref_field.name}Exist = async ({ref_field.name_db}: mongoose.Types.ObjectId[]) => {{\n"
                f"  try {{\n"
                f"    const {ref_field.name} = await {ref_field.type}Model.find({{ _id: {{ $in: {ref_field.name_db} }} }});\n"
                f"    return {ref_field.name}.length === {ref_field.name_db}.length;\n"
                f"  }} catch (_e) {{\n"
                f"    return false;\n"
                f"  }}\n"
                f"}};"
            ) if ref_field.is_ref and ref_field.is_arr else ""

            # Non-Reference Fields (placeholders)
            + (
                f"const {ref_field.name}Validator = async ({ref_field.name_db}: mongoose.Types.ObjectId{'[]' if ref_field.is_arr else ''}) => {{\n"
                f"  return true;\n"
                f"}};"
            ) if not ref_field.is_ref else ""

            for ref_field in entity.fields
        ]) + "\n\n"
        
        # Export validators
        f"export const validators = {{\n"
        + ',\n'.join([
            # Reference Field Validators
            f"  {ref_field.name}Exist" + ("s" if not ref_field.is_arr else "")
            if ref_field.is_ref else ""

            # Non-Reference Field Validators
            + f"  {ref_field.name}Validator"
            if not ref_field.is_ref else ""

            for ref_field in entity.fields
        ]) + "\n"
        f"}};\n"
    )
