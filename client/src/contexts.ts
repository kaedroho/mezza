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

export interface PipelineStage {
  id: number;
  title: string;
  url: string;
}

export interface Pipeline {
  id: number;
  title: string;
  stages: PipelineStage[];
}

export const PipelinesContext = React.createContext<Pipeline[]>([]);
