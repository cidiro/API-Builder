# post[Entity].ts.py
# post[Entity].ts builder

def build(entity):
    return (
        f"import {{ Request, Response }} from \"express\";\n"
        f"import {{ {entity.name}Model, {entity.name}ModelType }} from "
        f"\"../../db/{entity.name.lower()}/{entity.name.lower()}.ts\";\n\n"

        f"export const post{entity.name} = async (\n"
        f"  req: Request<{{}}, {{}}, {entity.name}ModelType>,\n"
        f"  res: Response<{entity.name}ModelType | {{ error: unknown }}>\n"
        f") => {{\n"
        f"  try {{\n"
        f"    const {{ {', '.join([field.name_db for field in entity.fields])} }} = req.body;\n"
        f"    const {entity.name.lower()} = new {entity.name}Model({{\n"
        + ',\n'.join([
            f"      {field.name_db}"
            for field in entity.fields
        ]) + "\n"
        f"    }});\n"
        f"    await {entity.name.lower()}.save();\n\n"
             
        f"    res.status(201).send({entity.name.lower()});\n"
        f"  }} catch (error) {{\n"
        f"    res.status(500).send(error);\n"
        f"  }}\n"
        f"}};\n"
    )
