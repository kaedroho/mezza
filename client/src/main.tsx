import * as DjangoBridge from "@django-bridge/react";
import React from "react";
import ReactDOM from "react-dom/client";

import { CSRFTokenContext, URLsContext, WorkspacesContext } from "./contexts";
import FieldDef from "./deserializers/Field";
import FormDef from "./deserializers/Form";
import ServerRenderedFieldDef from "./deserializers/ServerRenderedField";
import BlockNoteEditorDef from "./deserializers/widgets/BlockNoteEditor";
import FileInputDef from "./deserializers/widgets/FileInput";
import SelectDef from "./deserializers/widgets/Select";
import TextAreaDef from "./deserializers/widgets/TextArea";
import TextInputDef from "./deserializers/widgets/TextInput";
import ConfirmDeleteView from "./views/ConfirmDelete";
import FileChooserView from "./views/FileChooser";
import FileDetail from "./views/FileDetail";
import FileIndex from "./views/FileIndex";
import FileUploadView from "./views/FileUpload";
import LoginView from "./views/Login";

const config = new DjangoBridge.Config();

// Add your views here
config.addView("Login", LoginView);
config.addView("FileDetail", FileDetail);
config.addView("FileIndex", FileIndex);
config.addView("FileUpload", FileUploadView);
config.addView("FileChooser", FileChooserView);
config.addView("ConfirmDelete", ConfirmDeleteView);

// Add your context providers here
config.addContextProvider("csrf_token", CSRFTokenContext);
config.addContextProvider("urls", URLsContext);
config.addContextProvider("workspaces", WorkspacesContext);

// Add your deserializers here
config.addAdapter("forms.Form", FormDef);
config.addAdapter("forms.Field", FieldDef);
config.addAdapter("forms.ServerRenderedField", ServerRenderedFieldDef);
config.addAdapter("forms.TextInput", TextInputDef);
config.addAdapter("forms.TextArea", TextAreaDef);
config.addAdapter("forms.Select", SelectDef);
config.addAdapter("forms.FileInput", FileInputDef);
config.addAdapter("forms.BlockNoteEditor", BlockNoteEditorDef);

const rootElement = document.getElementById("root")!;
const initialResponse = JSON.parse(
  document.getElementById("initial-response")!.textContent!,
);

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <DjangoBridge.App config={config} initialResponse={initialResponse} />
  </React.StrictMode>,
);
