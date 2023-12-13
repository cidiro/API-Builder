import { [Entity]ModelType } from "./[entity].ts";
{...<Reference>
import { [Reference]Model } from "../[reference]/[reference].ts";
...}

export const [entity]PostSave = async function (doc: [Entity]ModelType) {
  try {
    {...<Middleware>
    // Update [entity]IDs in related [reference]s
    await [Reference]Model.updateMany(
      { _id: { $in: doc.[reference]IDs } },
      { $push: { [entity]IDs: doc._id } },
    );
    ...}
  } catch (_e) {
    console.log(_e);
  }
};

export const [entity]PostUpdate = async function (doc: [Entity]ModelType) {
  try {
    {...<UpdateMany>
    // [reference]IDs got updated: update [entity]IDs in related [reference]s
    const old[Reference]s = await [Reference]Model.find({
      [entity]IDs: { $elemMatch: { $eq: doc._id } },
    });
    const old[Reference]sID = old[Reference]s.map(([reference]) => [reference]._id);

    const [reference]IDsRemoved = old[Reference]sID.filter(
      ([reference]ID) => !doc.[reference]IDs.includes([reference]ID),
    );
    const [reference]IDsAdded = doc.[reference]IDs.filter(
      ([reference]ID) => !old[Reference]sID.includes([reference]ID),
    );

    await [Reference]Model.updateMany(
      { _id: { $in: [reference]IDsRemoved } },
      { $pull: { [entity]IDs: doc._id } },
    );
    await [Reference]Model.updateMany(
      { _id: { $in: [reference]IDsAdded } },
      { $push: { [entity]IDs: doc._id } },
    );
    ...}

    {...<UpdateOne>
    // [reference]ID got updated: update [entity]IDs in related [reference]
    const [reference] = await [Reference]Model.findOne({
      [entity]IDs: { $elemMatch: { $eq: doc._id } },
    });

    if ([reference]?._id !== doc.[reference]ID) {
      await [Reference]Model.updateOne(
        { _id: [reference]?._id },
        { $pull: { [entity]IDs: doc._id } },
      );
      await [Reference]Model.updateOne(
        { _id: doc.[reference]ID },
        { $push: { [entity]IDs: doc._id } },
      );
    }
    ...}
  } catch (_e) {
    console.log(_e);
  }
};

export const [entity]PostDelete = async function (doc: [Entity]ModelType) {
  try {
    {...<Middleware>
    // Update [entity]IDs in related [reference]s
    await [Reference]Model.updateMany(
      { _id: { $in: doc.[reference]IDs } },
      { $pull: { [entity]IDs: doc._id } },
    );
    ...}
  } catch (_e) {
    console.log(_e);
  }
};
