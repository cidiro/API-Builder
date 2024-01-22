# main.ts.py
# main.ts builder

def build(entities):
    return (
        f"import express from \"express\";\n"
        f"import mongoose from \"mongoose\";\n\n"

        + '\n\n'.join([
            f"import {{ get{entity.name} }} from \"./resolvers/{entity.name.lower()}/get{entity.name}.ts\";\n"
            f"import {{ get{entity.name_plural} }} from \"./resolvers/{entity.name.lower()}/get{entity.name_plural}.ts\";\n"
            f"import {{ post{entity.name} }} from \"./resolvers/{entity.name.lower()}/post{entity.name}.ts\";\n"
            f"import {{ put{entity.name} }} from \"./resolvers/{entity.name.lower()}/put{entity.name}.ts\";\n"
            f"import {{ delete{entity.name} }} from \"./resolvers/{entity.name.lower()}/delete{entity.name}.ts\";"
            for entity in entities
        ]) + "\n\n\n"


        f"const MONGO_URL = Deno.env.get(\"MONGO_URL\");\n\n"

        f"if (!MONGO_URL) {{\n"
        f"  console.error(\"MONGO_URL environment variable not set!\");\n"
        f"  Deno.exit(1);\n"
        f"}}\n\n"

        f"await mongoose.connect(MONGO_URL);\n"
        f"const app = express();\n"
        f"app.use(express.json());\n"
        f"app\n"
        + '\n'.join([
            f"  .get(\"/{entity.name.lower()}/:id\", get{entity.name})\n"
            f"  .get(\"/{entity.name_plural.lower()}\", get{entity.name_plural})\n"
            f"  .post(\"/{entity.name.lower()}\", post{entity.name})\n"
            f"  .put(\"/{entity.name.lower()}/:id\", put{entity.name})\n"
            f"  .delete(\"/{entity.name.lower()}/:id\", delete{entity.name})"
            for entity in entities
        ]) + ";\n\n"
        
        f"app.listen(3000, () => {{\n"
        f"  console.log(\"🚀 Server listening on port 3000 !\");\n"
        f"}});\n"
    )
