# get[Entities].ts.py
# get[Entity]s.ts builder

def build(entity):
    return (
        f"import {{ {entity.name}Model, {entity.name}ModelType }} from "
        f"\"../../../db/{entity.name.lower()}/{entity.name.lower()}.ts\";\n\n"
        
        f"const get{entity.name_plural} = async (): Promise<{entity.name}ModelType[]> => {{\n"
        f"  return await {entity.name}Model.find().exec();\n"
        f"}};\n\n"
        
        f"export default get{entity.name_plural};\n"
    )
