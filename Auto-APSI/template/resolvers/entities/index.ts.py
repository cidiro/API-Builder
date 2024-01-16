# index.ts.py
# index.ts builder

def build(entities):
    return (
        '\n'.join([
            f"import {{ {entity.name} }} from \"./{entity.name.lower()}.ts\";"
            for entity in entities
        ]) + "\n\n"

        f"const entities = {{\n"
        + ',\n'.join([f"  {entity.name}" for entity in entities]) + "\n"
        f"}};\n\n"
        
        f"export default entities;\n"
    )
