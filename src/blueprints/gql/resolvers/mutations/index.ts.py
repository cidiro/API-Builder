# index.ts.py
# index.ts builder

def build(entities):
    return (
        '\n'.join([
            f"import add{entity.name} from \"./{entity.name.lower()}/add{entity.name}.ts\";\n"
            f"import update{entity.name} from \"./{entity.name.lower()}/update{entity.name}.ts\";\n"
            f"import delete{entity.name} from \"./{entity.name.lower()}/delete{entity.name}.ts\";"
            for entity in entities
        ]) + "\n\n"

        "const mutations = {\n"
        "  Mutation: {\n"
        + ',\n'.join([
            f"    ...add{entity.name},\n"
            f"    ...update{entity.name},\n"
            f"    ...delete{entity.name}"
            for entity in entities
        ]) + "\n"
        "  }\n"
        "};\n\n"
        
        "export default mutations;\n"
    )
