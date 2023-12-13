import { [Entity]Model, [Entity]ModelType } from "../../../db/[entity]/[entity].ts";

const add[Entity] = {
  Mutation: {
    add[Entity]: async (
      _: unknown,
      args: { [arg_fields] }
    ): Promise<[Entity]ModelType> => {
      const [entity] = new [Entity]Model({
        [model_fields]
      });

      await [entity].save();
      return [entity];
    },
  },
};

export default add[Entity];
