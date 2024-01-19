# put[Entity].ts.py
# put[Entity].ts builder

def build(entity):
    return (
        f"import {{ Request, Response }} from \"express\";\n"
        f"import {{ {entity.name}Model, {entity.name}ModelType }} from "
        f"\"../../db/{entity.name.lower()}/{entity.name.lower()}.ts\";\n\n"

        f"export const put{entity.name} = async (\n"
        f"  req: Request<{{ id: string }}, {{}}, {entity.name}ModelType>,\n"
        f"  res: Response<{entity.name}ModelType | {{ error: unknown }}>\n"
        f") => {{\n"
        f"  const id = req.params.id;\n"
        f"  const {{ {', '.join([field.name_db for field in entity.fields])} }} = req.body;\n"
        f"  try {{\n"
        f"    const {entity.name.lower()} = await {entity.name}Model.findByIdAndUpdate(\n"
        f"      id,\n"
        f"      {{ {', '.join([field.name_db for field in entity.fields])} }},\n"
        f"      {{ new: true, runValidators: true }}\n"
        f"    );\n\n"
        
        f"    if (!{entity.name.lower()}) {{\n"
        f"      res.status(404).send(`{entity.name} with id ${{ id }} not found.`);\n"
        f"      return;\n"
        f"    }}\n"
        f"    res.status(200).send({entity.name.lower()});\n"
        f"  }} catch (error) {{\n"
        f"    res.status(500).send(error);\n"
        f"  }}\n"
        f"}};\n"
    )
