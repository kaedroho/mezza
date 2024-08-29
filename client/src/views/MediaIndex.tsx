import { NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import Button from "@mui/joy/Button";
import React from "react";
import AssetList from "../components/AssetList";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
import { Asset, AssetLibrary } from "../types";

interface MediaIndexProps {
  library: AssetLibrary;
  libraries: AssetLibrary[];
  assets: Asset[];
}

export default function MediaIndex({ library, assets }: MediaIndexProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);

  return (
    <Layout
      title="Media"
      renderHeaderButtons={() => (
        <Button
          variant="plain"
          color="primary"
          size="sm"
          startDecorator={<Add />}
          onClick={() =>
            openOverlay(
              library.upload_url,
              (content) => <ModalWindow>{content}</ModalWindow>,
              {
                onClose: () => {
                  // Refresh props so new post pops up in listing
                  refreshProps();
                },
              },
            )
          }
        >
          Upload
        </Button>
      )}
    >
      <AssetList assets={assets} />
    </Layout>
  );
}
