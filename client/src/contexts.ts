import React from "react";

export const CSRFTokenContext = React.createContext<string>("");

export interface URLs {
  projects_index: string;
  projects_create: string;
  files_index: string;
}

export const URLsContext = React.createContext<URLs>({
  projects_index: "",
  projects_create: "",
  files_index: "",
});
