import { getNameInitialsSimpleUtil } from "@/utilities/index_utils";

export const IndexComponent1 = () => {
  return <div>{getNameInitialsSimpleUtil("John Doe")}</div>;
};