import mongoose from "mongoose";
import { [Entity] } from "../../types.ts";
import { validators } from "./validators.ts";
import { globalValidators } from "../globalValidators.ts";
import { [entity]PostDelete, [entity]PostSave, [entity]PostUpdate } from "./middleware.ts";

export type [Entity]ModelType =
  & mongoose.Document
  & Omit<[Entity], "id"[omit_fields]>
  & { [include_fields] };

const Schema = mongoose.Schema;

const [entity]Schema = new Schema(
  {
    // Add the unique = true attribute to the unique fields below
    [schema_fields]
  },
  { timestamps: true },
);

{...<Field>
[entity]Schema.path("[field]").validate(
  globalValidators.nameIsValid,
  "message",
);
...}

// on save: update related documents
[entity]Schema.post("save", [entity]PostSave);

// on update: update related documents
[entity]Schema.post("findOneAndUpdate", [entity]PostUpdate);

// on delete: update related documents
[entity]Schema.post("deleteOne", [entity]PostDelete);

export const [Entity]Model = mongoose.model<[Entity]ModelType>(
  "[Entity]",
  [entity]Schema,
);
