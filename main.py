import os, re, sys
from entity_parser import entity_parser


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <types.ts file>")
        exit(1)

    print("Doing black magic...")

    template_dir = os.path.join(os.path.dirname(__file__), "template")
    types_file = sys.argv[1]
    target_dir = os.path.dirname(types_file)

    # Parse the types.ts file and get a list of the entites
    entities = entity_parser(types_file)

    # Walk through the template directory to create a project based on the types.ts entities
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            # Get the full path of the file in template_dir
            template_file = os.path.join(root, file)
            # Get the relative path of the file in template_dir
            relative_path = os.path.relpath(template_file, template_dir)
            # Get the full path of the file in target_dir
            target_template_file = os.path.join(target_dir, relative_path)

            if "[entity]" in target_template_file or "[Entity]" in target_template_file:
                for entity in entities:
                    target_file = target_template_file.replace("[entity]", entity.name.lower())
                    target_file = target_file.replace("[Entity]", entity.name)

                    # Make sure the directory exists
                    os.makedirs(os.path.dirname(target_file), exist_ok=True)

                    # Copy the file
                    with (open(template_file, "r") as f):
                        content = ""
                        # if file is inside queries folder
                        if (("\\resolvers\\" in target_file or "\\db\\" in target_file)
                                and "middleware.ts" not in target_file):
                            # Read whole file
                            content = f.read()

                            # Replace entity placeholders with entity name
                            content = content.replace("[Entity]", entity.name)
                            content = content.replace("[entity]", entity.name.lower())

                            # Replace fields placeholders with field names and types
                            arg_fields = model_fields = omit_fields = include_fields = schema_fields = ""
                            for field in entity.fields:
                                arg_fields += (f"{field.name if not field.is_ref else field.alt_name}: " +
                                               f"{field.type if not field.is_ref else field.alt_type}, ")
                                model_fields += (f"{field.name if not field.is_ref else field.alt_name}: "
                                                 f"args.{field.name if not field.is_ref else field.alt_name}, ")
                                schema_fields += (
                                        f"{field.name if not field.is_ref else field.alt_name}: " +
                                        ("[ " if field.is_array else "") + "{ type: " +
                                        (field.type.capitalize() if not field.is_ref else "Schema.Types.ObjectId") +
                                        f", required: " + ("true" if field.required else "false") +
                                        (f', ref: "{field.type}"' if field.is_ref else "") + " }," +
                                        (" ]," if field.is_array else "") + "\n    "
                                )
                                if field.is_ref:
                                    omit_fields += f' | "{field.name}"'
                                    include_fields += (f"{field.alt_name}: " +
                                                       ("mongoose.Types.ObjectId"
                                                        if not field.is_array
                                                        else "Array<mongoose.Types.ObjectId>") +
                                                       ", ")

                            content = content.replace("[arg_fields]", arg_fields[:-2])
                            content = content.replace("[model_fields]", model_fields[:-2])
                            content = content.replace("[omit_fields]", omit_fields)
                            content = content.replace("[include_fields]", include_fields[:-2])
                            content = content.replace("[schema_fields]", schema_fields[:-5])

                            # Expand placeholder blocks, replacing placeholders with corresponding entity data
                            while re.search(r"{\.\.\.[\s\S]*?\.\.\.}", content):
                                substring = content.split("{...")[1].split("...}")[0]

                                # Replace reference placeholders with referenced entity names
                                if "<Reference>" in substring:
                                    substring = substring.replace("<Reference>", "", 1).lstrip("\n").rstrip()
                                    block_string = ""
                                    for field in entity.fields:
                                        if field.is_ref:
                                            # Common reference placeholders
                                            block_string += substring.replace("[Reference]", field.type) + "\n"
                                            block_string = block_string.replace("[reference]", field.type.lower())
                                            block_string = block_string.replace("[reference_field]", field.name)
                                            block_string = block_string.replace("[reference_alt]", field.alt_name)

                                            # [promise_type] placeholder
                                            promise_type = f"{field.type}ModelType | null" \
                                                           if not field.is_array \
                                                           else f"Array<{field.type}ModelType>"
                                            block_string = block_string.replace("[promise_type]", promise_type)

                                            # [find_args] placeholder
                                            field_arg = (("parent." if "\\resolvers\\" in target_file else "")
                                                         + field.alt_name)
                                            find_args = f"ById({field_arg})" \
                                                        if not field.is_array \
                                                        else f"({{ _id: {{ $in: {field_arg} }} }})"
                                            block_string = block_string.replace("[find_args]", find_args)

                                            # [exists_func] placeholder
                                            exists_func = f"{field.name}Exist" + ("s" if not field.is_array else "")
                                            block_string = block_string.replace("[exists_func]", exists_func)

                                            # [exists_args] placeholder
                                            exists_args = (f"{field.alt_name}: mongoose.Types.ObjectId"
                                                           + ("[]" if field.is_array else ""))
                                            block_string = block_string.replace("[exists_args]", exists_args)

                                            # [exists_return] placeholder
                                            exists_return = (f"!!{field.name}"
                                                             if not field.is_array
                                                             else f"{field.name}.length === {field.alt_name}.length")
                                            block_string = block_string.replace("[exists_return]", exists_return)
                                    content = re.sub(r"( *){\.\.\.[\s\S]*?\.\.\.}", block_string[:-1], content, count=1)

                                # Replace field placeholders with field names
                                elif "<Field>" in substring:
                                    substring = substring.replace("<Field>", "", 1).lstrip("\n").rstrip()
                                    block_string = ""
                                    for field in entity.fields:
                                        field_name = field.name if not field.is_ref else field.alt_name
                                        block_string += substring.replace("[field]", field_name) + "\n\n"
                                    content = re.sub(r"( *){\.\.\.[\s\S]*?\.\.\.}", block_string[:-2], content, count=1)
                        else:
                            content = f.read()

                    # Create the file with the content
                    with open(target_file, "w") as f:
                        f.write(content)
            else:
                # Make sure the directory exists
                os.makedirs(os.path.dirname(target_template_file), exist_ok=True)

                # Copy the file
                with open(template_file, "r") as f:
                    content = ""
                    # if file name is typeDefs.ts
                    if os.path.basename(template_file) == "typeDefs.ts":
                        lines = f.readlines()
                        block_flag = False
                        for index, line in enumerate(lines):
                            if "type [Entity]" in line:
                                block_flag = True
                                for entity in entities:
                                    content += line.replace("[Entity]", entity.name)
                                    for entity_line in lines[index + 1:]:
                                        if entity_line.strip().startswith("}"):
                                            content += entity_line + "\n"
                                            break
                                        if "[field]: [type]!" in entity_line:
                                            for field in entity.fields:
                                                field_type = field.type.capitalize()
                                                content += (
                                                    f"    {field.name}: "
                                                    f"{field_type if not field.is_array else f'[{field_type}!]'}" +
                                                    ("!" if field.required else "") + "\n"
                                                )
                                        else:
                                            content += entity_line
                                content = content[:-1]

                            elif "type Query" in line or "type Mutation" in line:
                                content += line
                                block_flag = True
                                for entity in entities:
                                    for entity_line in lines[index + 1:]:
                                        if entity_line.strip().startswith("}"):
                                            content += "\n"
                                            break
                                        new_line = entity_line.replace("[Entity]", entity.name)
                                        fields = ""
                                        for field in entity.fields:
                                            field_type = field.type.capitalize() if not field.is_ref else "ID"
                                            is_update = entity_line.strip().startswith("update")
                                            fields += (
                                                f"{field.name}: "
                                                f"{field_type if not field.is_array else f'[{field_type}!]'}" +
                                                ("!" if field.required and not is_update else "") + ", "
                                            )
                                        new_line = new_line.replace("[fields]", fields[:-2])
                                        content += new_line

                                content = content[:-1]
                                content += "  }\n"

                            elif line.strip().startswith("}"):
                                block_flag = False
                            elif not block_flag:
                                content += line
                        content = content.replace("Number", "Int")
                    else:
                        content = f.read()
                        while re.search(r"{\.\.\.[\s\S]*?\.\.\.}", content):
                            substring = content.split("{...")[1].split("...}")[0].lstrip("\n").rstrip()
                            entities_string = ""
                            for entity in entities:
                                entities_string += substring.replace("[Entity]", entity.name) + "\n"
                                entities_string = entities_string.replace("[entity]", entity.name.lower())
                            content = re.sub(r"( *){\.\.\.[\s\S]*?\.\.\.}", entities_string[:-1], content, count=1)

                # Create the file with the content
                with open(target_template_file, "w") as f:
                    f.write(content)

    print("Done!")
