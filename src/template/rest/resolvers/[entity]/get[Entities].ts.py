# get[Entities].ts.py
# get[Entities].ts builder

def build(entity):
    return (
        f"import {{ Request, Response }} from \"express\";\n"
        f"import {{ {entity.name}Model, {entity.name}ModelType }} from "
        f"\"../../db/{entity.name.lower()}/{entity.name.lower()}.ts\";\n\n"

        f"export const get{entity.name_plural} = async (\n"
        f"  _req: Request,\n"
        f"  res: Response<{entity.name}ModelType[] | {{ error: unknown }}>\n"
        f") => {{\n"
        f"  try {{\n"
        f"    const {entity.name_plural.lower()} = await {entity.name}Model.find({{}})\n"
        + '\n'.join([
            f"      .populate(\"{field.name_db}\", \"_id\")"
            for field in entity.fields
            if field.is_ref
        ]) + "\n"
        f"      .select(\"-createdAt -updatedAt -__v\")\n"
        f"      .exec();\n\n"
        
        f"    res.status(200).send({entity.name_plural.lower()});\n"
        f"  }} catch (error) {{\n"
        f"    res.status(500).send(error);\n"
        f"  }}\n"
        f"}};\n"
    )
