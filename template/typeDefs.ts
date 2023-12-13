const typeDefs = `#graphql
  type [Entity] {
    id: ID!
    [field]: [type]!
  }

  type Query {
    get[Entity](id: ID!): [Entity]!
    get[Entity]s: [[Entity]!]!
  }

  type Mutation {
    add[Entity]([fields]): [Entity]!
    update[Entity](id: ID!, [fields]): [Entity]!
    delete[Entity](id: ID!): [Entity]!
  }
`;

export default typeDefs;
