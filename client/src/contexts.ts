import React from "react";
import { Space } from "./types";

export const CSRFTokenContext = React.createContext<string>("");

export interface URLs {
  projects_index: string;
  projects_create: string;
  ideas_index: string;
  ideas_create: string;
  asset_index: string;
}

export const URLsContext = React.createContext<URLs>({
  projects_index: "",
  projects_create: "",
  ideas_index: "",
  ideas_create: "",
  asset_index: "",
});

export interface Spaces {
  current: string;
  spaces: Space[];
}

export const SpacesContext = React.createContext<Spaces>({
  current: "unknown",
  spaces: [
    {
      slug: "unknown",
      name: "Mezza Studio",
    },
  ],
});
