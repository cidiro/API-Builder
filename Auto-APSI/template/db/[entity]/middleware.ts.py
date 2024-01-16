# middleware.ts.py
# middleware.ts builder

def build(entity, entities):
    return (
        f"import {{ {entity.name}ModelType }} from \"./{entity.name.lower()}.ts\";\n"
        + '\n'.join([
            f"import {{ {ref_field.type}Model }} from \"../{ref_field.type.lower()}/{ref_field.type.lower()}.ts\";"
            for ref_field in entity.fields
            if ref_field.is_ref
        ]) + "\n\n"

        f"export const {entity.name.lower()}PostSave = async (doc: {entity.name}ModelType) => {{\n"
        f"  try {{\n"
        + '\n'.join([
            # Update Array Field in Referenced Entity
            (
                f"    // Update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    await {ref_doc.name}Model.updateOne(\n"
                f"      {{ _id: doc.{doc_ref_field.name_db} }},\n"
                f"      {{ $push: {{ {ref_doc_ref_field.name_db}: doc._id }} }}\n"
                f"    );"
            ) if ref_doc_ref_field.is_arr and not doc_ref_field.is_arr else ""

            # Update Array Field in Referenced Entities
            + (
                f"    // Update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    await {ref_doc.name}Model.updateMany(\n"
                f"      {{ _id: {{ $in: doc.{doc_ref_field.name_db} }} }},\n"
                f"      {{ $push: {{ {ref_doc_ref_field.name_db}: doc._id }} }}\n"
                f"    );"
            ) if ref_doc_ref_field.is_arr and doc_ref_field.is_arr else ""

            # Update Non-Array Field in Referenced Entity
            + (
                f"    // Update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    await {ref_doc.name}Model.updateOne(\n"
                f"      {{ _id: doc.{doc_ref_field.name_db} }},\n"
                f"      {{ {ref_doc_ref_field.name_db}: doc._id }}\n"
                f"    );"
            ) if not ref_doc_ref_field.is_arr and not doc_ref_field.is_arr else ""

            # Update Non-Array Field in Referenced Entities
            + (
                f"    // Update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    await {ref_doc.name}Model.updateMany(\n"
                f"      {{ _id: {{ $in: doc.{doc_ref_field.name_db} }} }},\n"
                f"      {{ {ref_doc_ref_field.name_db}: doc._id }}\n"
                f"    );"
            ) if not ref_doc_ref_field.is_arr and doc_ref_field.is_arr else ""

            for ref_doc in entities
            for ref_doc_ref_field in ref_doc.fields
            if ref_doc_ref_field.is_ref and ref_doc_ref_field.type == entity.name
            for doc_ref_field in entity.fields
            if doc_ref_field.is_ref and doc_ref_field.type == ref_doc.name
        ]) + "\n"
        f"  }} catch (_e) {{\n"
        f"    console.log(_e);\n"
        f"  }}\n"
        f"}};\n\n"
             
        f"export const {entity.name.lower()}PostUpdate = async (doc: {entity.name}ModelType) => {{\n"
        f"  try {{\n"
        + '\n\n'.join([
            # Update Array Field in Referenced Entity
            (
                f"    // {doc_ref_field.name_db} got updated: update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    const {doc_ref_field.name} = await {ref_doc.name}Model.findOne({{\n"
                f"      {ref_doc_ref_field.name_db}: {{ $elemMatch: {{ $eq: doc._id }} }}\n"
                f"    }});\n\n"
                f"    if ({doc_ref_field.name}?._id !== doc.{doc_ref_field.name_db}) {{\n"
                f"      await {ref_doc.name}Model.updateOne(\n"
                f"        {{ _id: {doc_ref_field.name}?._id }},\n"
                f"        {{ $pull: {{ {ref_doc_ref_field.name_db}: doc._id }} }}\n"
                f"      );\n"
                f"      await {ref_doc.name}Model.updateOne(\n"
                f"        {{ _id: doc.{doc_ref_field.name_db} }},\n"
                f"        {{ $push: {{ {ref_doc_ref_field.name_db}: doc._id }} }}\n"
                f"      );\n"
                f"    }}"
            ) if ref_doc_ref_field.is_arr and not doc_ref_field.is_arr else ""

            # Update Array Field in Referenced Entities
            + (
                f"    // {doc_ref_field.name_db} got updated: update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    const old{doc_ref_field.name.capitalize()} = await {ref_doc.name}Model.find({{\n"
                f"      {ref_doc_ref_field.name_db}: {{ $elemMatch: {{ $eq: doc._id }} }}\n"
                f"    }});\n"
                f"    const old{doc_ref_field.name.capitalize()}IDs = old{doc_ref_field.name.capitalize()}.map(({ref_doc.name.lower()}) => {ref_doc.name.lower()}._id);\n\n"
                f"    const {doc_ref_field.name_db}Removed = old{doc_ref_field.name.capitalize()}IDs.filter(\n"
                f"      ({ref_doc.name.lower()}ID) => !doc.{doc_ref_field.name_db}.includes({ref_doc.name.lower()}ID)\n"
                f"    );\n"
                f"    const {doc_ref_field.name_db}Added = doc.{doc_ref_field.name_db}.filter(\n"
                f"      ({ref_doc.name.lower()}ID) => !old{doc_ref_field.name.capitalize()}IDs.includes({ref_doc.name.lower()}ID)\n"
                f"    );\n\n"
                f"    await {ref_doc.name}Model.updateMany(\n"
                f"      {{ _id: {{ $in: {doc_ref_field.name_db}Removed }} }},\n"
                f"      {{ $pull: {{ {ref_doc_ref_field.name_db}: doc._id }} }}\n"
                f"    );\n"
                f"    await {ref_doc.name}Model.updateMany(\n"
                f"      {{ _id: {{ $in: {doc_ref_field.name_db}Added }} }},\n"
                f"      {{ $push: {{ {ref_doc_ref_field.name_db}: doc._id }} }}\n"
                f"    );"
            ) if ref_doc_ref_field.is_arr and doc_ref_field.is_arr else ""

            # Update Non-Array Field in Referenced Entity
            + (
                f"    // {doc_ref_field.name_db} got updated: update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    const {doc_ref_field.name} = await {ref_doc.name}Model.findOne({{\n"
                f"      {ref_doc_ref_field.name_db}: doc._id\n"
                f"    }});\n\n"
                f"    if ({doc_ref_field.name}?._id !== doc.{doc_ref_field.name_db}) {{\n"
                f"      await {ref_doc.name}Model.updateOne(\n"
                f"        {{ _id: {doc_ref_field.name}?._id }},\n"
                f"        {{ {ref_doc_ref_field.name_db}: null }}\n"
                f"      );\n"
                f"      await {ref_doc.name}Model.updateOne(\n"
                f"        {{ _id: doc.{doc_ref_field.name_db} }},\n"
                f"        {{ {ref_doc_ref_field.name_db}: doc._id }}\n"
                f"      );\n"
                f"    }}"
            ) if not ref_doc_ref_field.is_arr and not doc_ref_field.is_arr else ""

            # Update Non-Array Field in Referenced Entities
            + (
                f"    // {doc_ref_field.name_db} got updated: update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    const old{doc_ref_field.name.capitalize()} = await {ref_doc.name}Model.find({{\n"
                f"      {ref_doc_ref_field.name_db}: doc._id\n"
                f"    }});\n"
                f"    const old{doc_ref_field.name.capitalize()}IDs = old{doc_ref_field.name.capitalize()}.map(({ref_doc.name.lower()}) => {ref_doc.name.lower()}._id);\n\n"
                f"    const {doc_ref_field.name_db}Removed = old{doc_ref_field.name.capitalize()}IDs.filter(\n"
                f"      ({ref_doc.name.lower()}ID) => !doc.{doc_ref_field.name_db}.includes({ref_doc.name.lower()}ID)\n"
                f"    );\n"
                f"    const {doc_ref_field.name_db}Added = doc.{doc_ref_field.name_db}.filter(\n"
                f"      ({ref_doc.name.lower()}ID) => !old{doc_ref_field.name.capitalize()}IDs.includes({ref_doc.name.lower()}ID)\n"
                f"    );\n\n"
                f"    await {ref_doc.name}Model.updateMany(\n"
                f"      {{ _id: {{ $in: {doc_ref_field.name_db}Removed }} }},\n"
                f"      {{ {ref_doc_ref_field.name_db}: null }}\n"
                f"    );\n"
                f"    await {ref_doc.name}Model.updateMany(\n"
                f"      {{ _id: {{ $in: {doc_ref_field.name_db}Added }} }},\n"
                f"      {{ {ref_doc_ref_field.name_db}: doc._id }}\n"
                f"    );"
            ) if not ref_doc_ref_field.is_arr and doc_ref_field.is_arr else ""

            for ref_doc in entities
            for ref_doc_ref_field in ref_doc.fields
            if ref_doc_ref_field.is_ref and ref_doc_ref_field.type == entity.name
            for doc_ref_field in entity.fields
            if doc_ref_field.is_ref and doc_ref_field.type == ref_doc.name
        ]) + "\n"
        f"  }} catch (_e) {{\n"
        f"    console.log(_e);\n"
        f"  }}\n"
        f"}};\n\n"

        f"export const {entity.name.lower()}PostDelete = async (doc: {entity.name}ModelType) => {{\n"
        f"  try {{\n"
        + '\n'.join([
            # Update Array Field in Referenced Entity
            (
                f"    // Update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    await {ref_doc.name}Model.updateOne(\n"
                f"      {{ _id: doc.{doc_ref_field.name_db} }},\n"
                f"      {{ $pull: {{ {ref_doc_ref_field.name_db}: doc._id }} }}\n"
                f"    );"
            ) if ref_doc_ref_field.is_arr and not doc_ref_field.is_arr else ""

            # Update Array Field in Referenced Entities
            + (
                f"    // Update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    await {ref_doc.name}Model.updateMany(\n"
                f"      {{ _id: {{ $in: doc.{doc_ref_field.name_db} }} }},\n"
                f"      {{ $pull: {{ {ref_doc_ref_field.name_db}: doc._id }} }}\n"
                f"    );"
            ) if ref_doc_ref_field.is_arr and doc_ref_field.is_arr else ""

            # Update Non-Array Field in Referenced Entity
            + (
                f"    // Update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    await {ref_doc.name}Model.updateOne(\n"
                f"      {{ _id: doc.{doc_ref_field.name_db} }},\n"
                f"      {{ {ref_doc_ref_field.name_db}: null }}\n"
                f"    );"
            ) if not ref_doc_ref_field.is_arr and not doc_ref_field.is_arr else ""

            # Update Non-Array Field in Referenced Entities
            + (
                f"    // Update {ref_doc_ref_field.name_db} in related {doc_ref_field.name}\n"
                f"    await {ref_doc.name}Model.updateMany(\n"
                f"      {{ _id: {{ $in: doc.{doc_ref_field.name_db} }} }},\n"
                f"      {{ {ref_doc_ref_field.name_db}: null }}\n"
                f"    );"
            ) if not ref_doc_ref_field.is_arr and doc_ref_field.is_arr else ""

            for ref_doc in entities
            for ref_doc_ref_field in ref_doc.fields
            if ref_doc_ref_field.is_ref and ref_doc_ref_field.type == entity.name
            for doc_ref_field in entity.fields
            if doc_ref_field.is_ref and doc_ref_field.type == ref_doc.name
        ]) + "\n"
        f"  }} catch (_e) {{\n"
        f"    console.log(_e);\n"
        f"  }}\n"
        f"}};\n"
    )
