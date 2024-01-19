# build_project.py

import os
import sys
from .build_entities import build_entities


def build_project(option, output_dir):
    if not os.path.isfile(os.path.join(output_dir, "db.json")):
        print("Error: db.json not found in target directory.")
        sys.exit(1)

    print("Building project...")

    template_dir = os.path.join(os.path.dirname(__file__), "template")
    entities = build_entities(os.path.join(output_dir, "db.json"))

    for root, dirs, files in os.walk(template_dir):
        for file in files:
            template_file = os.path.join(root, file)
            relative_path = os.path.relpath(template_file, template_dir)
            output_file = os.path.join(output_dir, relative_path[:-3])

            if option == 'rest' and 'gql' in output_file:
                continue
            elif option == 'gql' and 'rest' in output_file:
                continue

            output_file = output_file.replace(f"{option}\\", "")
            print(output_file)

            if not ("[entity]" in output_file or "[Entity]" in output_file):
                # Read template file
                with open(template_file, "r") as f:
                    program = f.read()

                # Execute template file
                namespace = {}
                exec(program, namespace)
                output = namespace['build'](entities)

                # Write output file
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, "w") as f:
                    f.write(output)

            else:
                for entity in entities:
                    entity_output_file = output_file.replace("[entity]", entity.name.lower())
                    entity_output_file = entity_output_file.replace("[Entity]", entity.name)
                    entity_output_file = entity_output_file.replace("[Entities]", entity.name_plural)

                    # Read template file
                    with open(template_file, "r") as f:
                        program = f.read()

                    # Execute template file
                    namespace = {}
                    exec(program, namespace)

                    # middleware.ts is a special case
                    if not os.path.basename(entity_output_file) == "middleware.ts":
                        output = namespace['build'](entity)
                    else:
                        output = namespace['build'](entity, entities)

                    # Write output file
                    os.makedirs(os.path.dirname(entity_output_file), exist_ok=True)
                    with open(entity_output_file, "w") as f:
                        f.write(output)

    print("Done!")
