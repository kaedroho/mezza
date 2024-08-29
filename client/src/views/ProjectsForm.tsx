import { Form, OverlayContext } from "@django-bridge/react";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import * as React from "react";
import Layout from "../components/Layout";
import { CSRFTokenContext, URLsContext } from "../contexts";
import FormDef from "../deserializers/Form";
import { Project } from "../types";

interface ProjectsFormViewProps {
  title: string;
  project: Project | null;
  action_url: string;
  form: FormDef;
}

export default function ProjectsFormView({
  title,
  project,
  action_url,
  form,
}: ProjectsFormViewProps) {
  const { overlay, requestClose } = React.useContext(OverlayContext);
  const urls = React.useContext(URLsContext);
  const csrf_token = React.useContext(CSRFTokenContext);

  return (
    <Layout title={title}>
      <Form action={action_url} method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value={csrf_token} />

        {form.render()}

        <Box display="flex" gap="12px" pt="20px">
          <Button type="submit">{project ? "Save changes" : "Save"}</Button>
          {overlay && (
            <Button
              type="button"
              variant="outlined"
              onClick={() => requestClose({ skipDirtyFormCheck: true })}
            >
              Cancel
            </Button>
          )}
        </Box>
      </Form>
    </Layout>
  );
}
