import { [Entity]ModelType } from "../../db/[entity]/[entity].ts";
{...<Reference>
import { [Reference]Model, [Reference]ModelType } from "../../db/[reference]/[reference].ts";
...}

export const [Entity] = {
  {...<Reference>
  [reference_field]: async (parent: [Entity]ModelType): Promise<[promise_type]> => {
    const [reference_field] = await [Reference]Model.find[find_args];
    return [reference_field];
  },
  ...}
};
