import { OverlayContext } from "@django-bridge/react";
import Box from "@mui/joy/Box";
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
      <Box
        sx={{
          display: "flex",
          flexFlow: "row nowrap",
          width: "100%",
          justifyContent: "center",
          my: 2,
          img: {
            maxWidth: "100%",
            height: "auto",
            maxHeight: "500px",
          },
          video: {
            maxWidth: "100%",
            height: "auto",
            maxHeight: "500px",
          },
        }}
      >
        {asset.type === "image" && (
          <img src={asset.file.download_url} alt={asset.title} />
        )}
        {asset.type === "video" && (
          <video src={asset.file.download_url} controls />
        )}
      </Box>
      <Box sx={{ mt: 2, px: 2 }}>
        <p>
          <b>File type:</b> {asset.file.file_type}
        </p>
        <p>
          <b>File size:</b> {asset.file.size}
        </p>
        {asset.type === "image" && (
          <p>
            <b>Dimensions:</b> {asset.file.width} x {asset.file.height}
          </p>
        )}
      </Box>
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
