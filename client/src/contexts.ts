import React from "react";

export const CSRFTokenContext = React.createContext<string>("");

export interface URLs {
    files_index: string;
}

export const URLsContext = React.createContext<URLs>({
    files_index: "",
});
