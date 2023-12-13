import mongoose from "mongoose";

// Validate name
const nameIsValid = (name: string) => name.length >= 3 && name.length <= 50;

// Validate number
const numberIsValid = (num: number) => num >= 1 && num <= 5;

// Validate email
const emailIsValid = (email: string) =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

// Validate that id is a valid MongoDB ObjectID
const idIsValid = (id: mongoose.Types.ObjectId) => mongoose.isValidObjectId(id);

// Validate that all IDs are valid MongoDB ObjectIDs
const idsAreValid = (ids: mongoose.Types.ObjectId[]) =>
  !(ids.some((id) => !mongoose.isValidObjectId(id)));

// Validate that all IDs are unique (not repeated)
const idsAreUnique = (ids: mongoose.Types.ObjectId[]) =>
  ids.length === new Set(ids).size;

export const globalValidators = {
  nameIsValid,
  numberIsValid,
  emailIsValid,
  idIsValid,
  idsAreValid,
  idsAreUnique,
};
