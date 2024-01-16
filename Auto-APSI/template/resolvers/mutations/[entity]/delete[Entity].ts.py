# delete[Entity].ts.py
# delete[Entity].ts builder

def build(entity):
    return (
        f"import {{ GraphQLError }} from \"graphql\";\n"
        f"import {{ {entity.name}Model, {entity.name}ModelType }} from "
        f"\"../../../db/{entity.name.lower()}/{entity.name.lower()}.ts\";\n\n"

        f"const delete{entity.name} = async (_: unknown, args: {{ id: string }}): Promise<{entity.name}ModelType> => {{\n"
        f"  const {entity.name.lower()} = await {entity.name}Model.findByIdAndDelete(args.id).exec();\n"
        f"  if (!{entity.name.lower()}) {{\n"
        f"    throw new GraphQLError(`No {entity.name.lower()} found with id ${{args.id}}`, {{\n"
        f"      extensions: {{ code: \"NOT_FOUND\" }},\n"
        f"    }});\n"
        f"  }}\n"
        f"  return {entity.name.lower()};\n"
        f"}};\n\n"
        
        f"export default delete{entity.name};\n"
    )
