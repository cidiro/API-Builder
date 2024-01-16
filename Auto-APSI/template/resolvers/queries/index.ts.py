# index.ts.py
# index.ts builder

def build(entities):
    return (
        '\n'.join([
            f"import get{entity.name} from \"./{entity.name.lower()}/get{entity.name}.ts\";\n"
            f"import get{entity.name_plural} from \"./{entity.name.lower()}/get{entity.name_plural}.ts\";"
            for entity in entities
        ]) + "\n\n"
    
        "const queries = {\n"
        "  Query: {\n"
        + ',\n'.join([
            f"    ...get{entity.name},\n"
            f"    ...get{entity.name_plural}"
            for entity in entities
        ]) + "\n"
        "  }\n"
        "};\n\n"
             
        "export default queries;\n"
    )
