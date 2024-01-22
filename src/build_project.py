# build_project.py

import os
import sys
from .build_entities import build_entities


def build_project(option, output_dir):
    if not os.path.isfile(os.path.join(output_dir, "db.json")):
        print("Error: db.json not found in target directory.")
        sys.exit(1)

    print("Building project...")

    blueprints_dir = os.path.join(os.path.dirname(__file__), "blueprints")
    entities = build_entities(os.path.join(output_dir, "db.json"))

    for root, dirs, files in os.walk(blueprints_dir):
        for file in files:
            blueprint_file = os.path.join(root, file)
            relative_path = os.path.relpath(blueprint_file, blueprints_dir)

            if option == 'rest' and 'gql' in relative_path:
                continue
            elif option == 'gql' and 'rest' in relative_path:
                continue

            relative_path = relative_path.replace(f"{option}\\", "")

            output_file = os.path.join(output_dir, relative_path[:-3])
            print(output_file)

            if not ("[entity]" in output_file or "[Entity]" in output_file):
                # Read blueprints file
                with open(blueprint_file, "r") as f:
                    program = f.read()

                # Execute blueprints file
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

                    # Read blueprints file
                    with open(blueprint_file, "r") as f:
                        program = f.read()

                    # Execute blueprints file
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
