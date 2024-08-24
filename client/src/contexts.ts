import React from "react";

export const CSRFTokenContext = React.createContext<string>("");

export interface URLs {
  projects_index: string;
  projects_create: string;
  ideas_index: string;
  ideas_create: string;
  assets_index: string;
}

export const URLsContext = React.createContext<URLs>({
  projects_index: "",
  projects_create: "",
  ideas_index: "",
  ideas_create: "",
  assets_index: "",
});

export interface Stage {
  slug: number;
  title: string;
  projects_url: string;
}

export const StagesContext = React.createContext<Stage[]>([]);
