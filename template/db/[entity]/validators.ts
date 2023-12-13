import mongoose from "mongoose";
{...<Reference>
import { [Reference]Model } from "../[reference]/[reference].ts";
...}

{...<Reference>
// Validate that [reference_alt] exists in the database
const [exists_func] = async ([exists_args]) => {
  try {
    const [reference_field] = await [Reference]Model.find[find_args];
    return [exists_return];
  } catch (_e) {
    return false;
  }
};
...}

export const validators = {
  {...<Reference>
  [exists_func],
  ...}
};
