import { Form, OverlayContext } from "@django-bridge/react";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import * as React from "react";
import Layout from "../components/Layout";
import { CSRFTokenContext } from "../contexts";
import FormDef from "../deserializers/Form";

interface AssetsUploadFormViewProps {
  action_url: string;
  form: FormDef;
}

export default function AssetsUploadFormView({
  action_url,
  form,
}: AssetsUploadFormViewProps) {
  const { overlay, requestClose } = React.useContext(OverlayContext);
  const csrf_token = React.useContext(CSRFTokenContext);

  return (
    <Layout title={"Upload asset"}>
      <Form action={action_url} method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value={csrf_token} />

        {form.render()}

        <Box display="flex" gap="12px" pt="20px">
          <Button type="submit">{"Upload"}</Button>
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
