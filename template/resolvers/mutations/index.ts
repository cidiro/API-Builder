{...
import add[Entity] from "./[entity]/add[Entity].ts";
import update[Entity] from "./[entity]/update[Entity].ts";
import delete[Entity] from "./[entity]/delete[Entity].ts";
...}

const mutations = {
  Mutation: {
    {...
    ...add[Entity].Mutation,
    ...update[Entity].Mutation,
    ...delete[Entity].Mutation,
    ...}
  },
};

export default mutations;
