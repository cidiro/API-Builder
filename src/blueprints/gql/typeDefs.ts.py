# typeDefs.ts.py
# typeDefs.ts builder

def build(entities):
    return (
        f"const typeDefs = `#graphql\n"

        # Entities
        + '\n\n'.join([
            f"  type {entity.name} {{\n"
            
            # Fields (id, name, etc.)
            f"    id: ID!\n"
            + '\n'.join([
                f"    {field.name}: "
                + (f"[{field.type_gql}!]" if field.is_arr else field.type_gql)
                + ("!" if field.is_req else "")
                for field in entity.fields
            ]) + "\n"
            f"  }}"
            for entity in entities
        ]) + "\n\n"

        # Query resolvers
        f"  type Query {{\n"
        + '\n\n'.join([
            f"    get{entity.name}(id: ID!): {entity.name}!\n"
            f"    get{entity.name_plural}: [{entity.name}!]!"
            for entity in entities
        ]) + "\n"
        f"  }}\n\n"

        # Mutation resolvers
        f"  type Mutation {{\n"
        + '\n\n'.join([
            # addEntity() resolver
            f"    add{entity.name}("
            + ', '.join([
                f"{field.name_db}: "
                + ("[" if field.is_arr else "")
                + (field.type_gql if not field.is_ref else "ID")
                + ("!]" if field.is_arr else "")
                + ("!" if field.is_req else "")
                for field in entity.fields
            ]) + f"): {entity.name}!\n"
    
            # updateEntity() resolver
            f"    update{entity.name}(id: ID!, "
            + ', '.join([
                f"{field.name_db}: "
                + ("[" if field.is_arr else "")
                + (field.type_gql if not field.is_ref else "ID")
                + ("!]" if field.is_arr else "")
                for field in entity.fields
            ]) + f"): {entity.name}!\n"
    
            # deleteEntity() resolver
            f"    delete{entity.name}(id: ID!): {entity.name}!"

            for entity in entities
        ]) + "\n"
        f"  }}\n"
        f"`;\n\n"
        
        f"export default typeDefs;\n"
    )
