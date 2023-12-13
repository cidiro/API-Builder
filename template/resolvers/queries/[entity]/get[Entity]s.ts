import { [Entity]Model, [Entity]ModelType } from "../../../db/[entity]/[entity].ts";

const get[Entity]s = {
  Query: {
    get[Entity]s: async (): Promise<[Entity]ModelType[]> => {
      const [entity]s = await [Entity]Model.find({}).exec();
      return [entity]s;
    },
  },
};

export default get[Entity]s;
