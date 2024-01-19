# [entity].ts.py
# [entity].ts builder

def build(entity):
    return (
        # Imports
        f"import mongoose from \"mongoose\";\n"
        f"import {{ {entity.name} }} from \"../../types.ts\";\n"
        f"import {{ validators }} from \"./validators.ts\";\n"
        f"import {{ globalValidators }} from \"../globalValidators.ts\";\n"
        f"import {{ {entity.name.lower()}PostSave, {entity.name.lower()}PostUpdate, "
        f"{entity.name.lower()}PostDelete }} from \"./middleware.ts\";\n\n"
    
        # Entity ModelType
        f"export type {entity.name}ModelType =\n"
        f"  & mongoose.Document\n"
        f"  & Omit<{entity.name}, "
        + ' | '.join(["\"id\""] + [f"\"{field.name}\"" for field in entity.fields if field.is_ref]) + ">\n"
        f"  & {{ " + ', '.join([
            f"{field.name_db}: mongoose.Types.ObjectId" + ("[]" if field.is_arr else "")
            for field in entity.fields if field.is_ref
        ]) + " };\n\n"
        
        # Entity Schema 
        f"const {entity.name.lower()}Schema = new mongoose.Schema(\n"
        f"  {{\n"
        + ',\n\n'.join([
            f"    {field.name_db}: " + ("[" if field.is_arr else "") + "{\n"
            f"      type: "
            + (field.type.capitalize() if not field.is_ref else "mongoose.Schema.Types.ObjectId") + ",\n"
            f"      required: {str(field.is_req).lower()},\n"
            + (f"      unique: {str(field.is_req).lower()},\n" if field.is_unique else "")
            + (f"      ref: \"{field.type}\",\n" if field.is_ref else "") +
            f"      validate: [\n"
            f"        {{\n"
            f"          validator: validators.{field.name_db}Validator,\n"
            f"          message: \"MESSAGE\"\n"
            f"        }}\n"
            f"      ]\n"
            f"    }}" + ("]" if field.is_arr else "")
            for field in entity.fields
        ]) + "\n"
        f"  }},\n\n"

        f"  {{ timestamps: true }}\n"
        f");\n\n"

        # Hooks
        f"{entity.name.lower()}Schema\n"
        f"  .post(\"save\", {entity.name.lower()}PostSave)\n"
        f"  .post(\"findOneAndUpdate\", {entity.name.lower()}PostUpdate)\n"
        f"  .post(\"findOneAndDelete\", {entity.name.lower()}PostDelete);\n\n"
        
        # Entity Model
        f"export const {entity.name}Model = mongoose.model<{entity.name}ModelType>(\n"
        f"  \"{entity.name.lower()}\",\n"
        f"  {entity.name.lower()}Schema\n"
        f");\n"
    )
