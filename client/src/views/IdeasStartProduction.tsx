import { Form, OverlayContext } from "@django-bridge/react";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import * as React from "react";
import Layout from "../components/Layout";
import { CSRFTokenContext } from "../contexts";

interface IdeasStartProductionViewProps {
  action_url: string;
}

export default function IdeasStartProductionView({
  action_url,
}: IdeasStartProductionViewProps) {
  const { overlay, requestClose } = React.useContext(OverlayContext);
  const csrf_token = React.useContext(CSRFTokenContext);

  return (
    <Layout title="Start Production">
      <Form action={action_url} method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value={csrf_token} />
        <p>
          This will start a new project and delete the idea. Are you sure you
          want to continue?
        </p>
        <Box display="flex" gap="12px" pt="20px">
          <Button type="submit">Start</Button>
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
