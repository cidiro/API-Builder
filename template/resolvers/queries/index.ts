{...
import get[Entity] from "./[entity]/get[Entity].ts";
import get[Entity]s from "./[entity]/get[Entity]s.ts";
...}

const queries = {
  Query: {
    {...
    ...get[Entity].Query,
    ...get[Entity]s.Query,
    ...}
  },
};

export default queries;
