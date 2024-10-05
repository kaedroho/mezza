import { OverlayContext } from "@django-bridge/react";
import Button from "@mui/joy/Button";
import React from "react";
import Layout from "../components/Layout";
import { Asset } from "../types";

interface MediaDetailViewProps {
  asset: Asset;
}

export default function MediaDetailView({ asset }: MediaDetailViewProps) {
  const { overlay, requestClose } = React.useContext(OverlayContext);

  return (
    <Layout title={asset.title} noIndent>
      {JSON.stringify(asset, undefined, 2)}
      {overlay && (
        <Button
          sx={{ mt: 2 }}
          type="button"
          variant="outlined"
          onClick={() => requestClose()}
        >
          Close
        </Button>
      )}
    </Layout>
  );
}
