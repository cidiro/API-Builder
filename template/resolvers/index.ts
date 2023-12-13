import entities from "./entities/index.ts";
import queries from "./queries/index.ts";
import mutations from "./mutations/index.ts";

const resolvers = {
  ...entities,
  ...queries,
  ...mutations,
};

export default resolvers;
