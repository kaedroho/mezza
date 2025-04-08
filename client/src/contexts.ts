import React from "react";
import { Workspace } from "./types";

export const CSRFTokenContext = React.createContext<string>("");

export interface URLs {
  file_index: string;
}

export const URLsContext = React.createContext<URLs>({
  file_index: "",
});

export interface Workspaces {
  current: string;
  workspaces: Workspace[];
}

export const WorkspacesContext = React.createContext<Workspaces>({
  current: "unknown",
  workspaces: [
    {
      slug: "unknown",
      name: "Mezza",
    },
  ],
});
