import { GraphQLError } from "graphql";
import { [Entity]Model, [Entity]ModelType } from "../../../db/[entity]/[entity].ts";

const update[Entity] = {
  Mutation: {
    update[Entity]: async (
      _: unknown,
      args: { id: string, [arg_fields] },
    ): Promise<[Entity]ModelType> => {
      const [entity] = await [Entity]Model.findByIdAndUpdate(
        args.id,
        { [model_fields] },
        { new: true, runValidators: true },
      ).exec();

      if (![entity]) {
        throw new GraphQLError(`No [entity] found with id ${args.id}`, {
          extensions: { code: "NOT_FOUND" },
        });
      }
      return [entity];
    },
  },
};

export default update[Entity];
