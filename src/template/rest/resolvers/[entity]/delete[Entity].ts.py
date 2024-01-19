# delete[Entity].ts.py
# delete[Entity].ts builder

def build(entity):
    return (
        f"import {{ Request, Response }} from \"express\";\n"
        f"import {{ {entity.name}Model }} from \"../../db/{entity.name.lower()}/{entity.name.lower()}.ts\";\n\n"

        f"export const delete{entity.name} = async (\n"
        f"  req: Request<{{ id: string }}, {{}}>,\n"
        f"  res: Response<string | {{ error: unknown }}>\n"
        f") => {{\n"
        f"  const id = req.params.id;\n"
        f"  const {entity.name.lower()} = await {entity.name}Model.findByIdAndDelete(id).exec();\n"
        f"  if (!{entity.name.lower()}) {{\n"
        f"    res.status(404).send(`{entity.name} with id ${{ id }} not found.`);\n"
        f"    return;\n"
        f"  }}\n"
        f"  res.status(200).send(\"{entity.name} deleted.\");\n"
        f"}};\n"
    )
