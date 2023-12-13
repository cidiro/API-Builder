import { GraphQLError } from "graphql";
import { [Entity]Model, [Entity]ModelType } from "../../../db/[entity]/[entity].ts";

const delete[Entity] = {
  Mutation: {
    delete[Entity]: async (_: unknown, args: { id: string }): Promise<[Entity]ModelType> => {
      const [entity] = await [Entity]Model.findByIdAndDelete(args.id).exec();
      if (![entity]) {
        throw new GraphQLError(`No [entity] found with id ${args.id}`, {
          extensions: { code: "NOT_FOUND" },
        });
      }
      return [entity];
    },
  },
};

export default delete[Entity];
