# get[Entity].ts.py
# get[Entity].ts builder

def build(entity):
    return (
        f"import {{ Request, Response }} from \"express\";\n"
        f"import {{ {entity.name}Model, {entity.name}ModelType }} from "
        f"\"../../db/{entity.name.lower()}/{entity.name.lower()}.ts\";\n\n"

        f"export const get{entity.name} = async (\n"
        f"  req: Request<{{ id: string }}>,\n"
        f"  res: Response<{entity.name}ModelType | {{ error: unknown }}>\n"
        f") => {{\n"
        f"  const id = req.params.id;\n"
        f"  try {{\n"
        f"    const {entity.name.lower()} = await {entity.name}Model.findById(id)\n"
        + '\n'.join([
            f"      .populate(\"{field.name_db}\", \"_id\")"
            for field in entity.fields
            if field.is_ref
        ]) + "\n"
        f"      .select(\"-createdAt -updatedAt -__v\")\n"
        f"      .exec();\n\n"
        
        f"    if (!{entity.name.lower()}) {{\n"
        f"      res.status(404).send(`{entity.name} with id ${{ id }} not found.`);\n"
        f"      return;\n"
        f"    }}\n\n"

        f"    res.status(200).send({entity.name.lower()});\n"
        f"  }} catch (error) {{\n"
        f"    res.status(500).send(error);\n"
        f"  }}\n"
        f"}};\n"
    )
