import * as DjangoBridge from "@django-bridge/react";
import React from "react";
import ReactDOM from "react-dom/client";

import { CSRFTokenContext, SpacesContext, URLsContext } from "./contexts";
import FieldDef from "./deserializers/Field";
import FormDef from "./deserializers/Form";
import ServerRenderedFieldDef from "./deserializers/ServerRenderedField";
import BlockNoteEditorDef from "./deserializers/widgets/BlockNoteEditor";
import FileInputDef from "./deserializers/widgets/FileInput";
import SelectDef from "./deserializers/widgets/Select";
import TextAreaDef from "./deserializers/widgets/TextArea";
import TextInputDef from "./deserializers/widgets/TextInput";
import ConfirmDeleteView from "./views/ConfirmDelete";
import IdeasIndex from "./views/IdeasIndex";
import IdeasStartProductionView from "./views/IdeasStartProduction";
import LoginView from "./views/Login";
import MediaChooserView from "./views/MediaChooser";
import MediaDetail from "./views/MediaDetail";
import MediaIndex from "./views/MediaIndex";
import MediaUploadFormView from "./views/MediaUploadForm";
import ProjectDetailView from "./views/ProjectDetail";
import ProjectsForm from "./views/ProjectsForm";
import ProjectsListingView from "./views/ProjectsListing";

const config = new DjangoBridge.Config();

// Add your views here
config.addView("Login", LoginView);
config.addView("ProjectDetail", ProjectDetailView);
config.addView("ProjectsListing", ProjectsListingView);
config.addView("IdeasIndex", IdeasIndex);
config.addView("IdeasStartProduction", IdeasStartProductionView);
config.addView("MediaDetail", MediaDetail);
config.addView("MediaIndex", MediaIndex);
config.addView("MediaUploadForm", MediaUploadFormView);
config.addView("MediaChooser", MediaChooserView);
config.addView("ConfirmDelete", ConfirmDeleteView);
config.addView("ProjectsForm", ProjectsForm);

// Add your context providers here
config.addContextProvider("csrf_token", CSRFTokenContext);
config.addContextProvider("urls", URLsContext);
config.addContextProvider("spaces", SpacesContext);

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
