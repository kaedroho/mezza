import * as DjangoBridge from "@django-bridge/react";
import React from "react";
import ReactDOM from "react-dom/client";

import { CSRFTokenContext, StagesContext, URLsContext } from "./contexts";
import FieldDef from "./deserializers/Field";
import FormDef from "./deserializers/Form";
import ServerRenderedFieldDef from "./deserializers/ServerRenderedField";
import BlockNoteEditorDef from "./deserializers/widgets/BlockNoteEditor";
import FileInputDef from "./deserializers/widgets/FileInput";
import SelectDef from "./deserializers/widgets/Select";
import TextInputDef from "./deserializers/widgets/TextInput";
import AssetsIndex from "./views/AssetsIndex";
import AssetsUploadFormView from "./views/AssetsUploadForm";
import ConfirmDeleteView from "./views/ConfirmDelete";
import IdeasIndex from "./views/IdeasIndex";
import IdeasStartProductionView from "./views/IdeasStartProduction";
import LoginView from "./views/Login";
import PostIndexView from "./views/PostIndex";
import ProjectDetailView from "./views/ProjectDetail";
import ProjectsBoardView from "./views/ProjectsBoard";
import ProjectsForm from "./views/ProjectsForm";
import ProjectsListingView from "./views/ProjectsListing";

const config = new DjangoBridge.Config();

// Add your views here
config.addView("Login", LoginView);
config.addView("ProjectDetail", ProjectDetailView);
config.addView("ProjectsBoard", ProjectsBoardView);
config.addView("ProjectsListing", ProjectsListingView);
config.addView("IdeasIndex", IdeasIndex);
config.addView("IdeasStartProduction", IdeasStartProductionView);
config.addView("AssetsIndex", AssetsIndex);
config.addView("AssetsUploadForm", AssetsUploadFormView);
config.addView("ConfirmDelete", ConfirmDeleteView);
config.addView("PostIndex", PostIndexView);
config.addView("ProjectsForm", ProjectsForm);

// Add your context providers here
config.addContextProvider("csrf_token", CSRFTokenContext);
config.addContextProvider("urls", URLsContext);
config.addContextProvider("stages", StagesContext);

// Add your deserializers here
config.addAdapter("forms.Form", FormDef);
config.addAdapter("forms.Field", FieldDef);
config.addAdapter("forms.ServerRenderedField", ServerRenderedFieldDef);
config.addAdapter("forms.TextInput", TextInputDef);
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
