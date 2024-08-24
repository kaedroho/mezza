import { NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import Button from "@mui/joy/Button";
import React from "react";
import styled from "styled-components";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
import { Asset, AssetLibrary } from "../types";

const AssetList = styled.ul`
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  list-style: none;
  padding: 0;
`;

const AssetCard = styled.li`
  background-color: var(--joy-palette-background-paper);
  border-radius: 8px;
  border: 1px solid var(--joy-palette-neutral-outlinedBorder);
  padding: 10px;

  h2 {
    font-size: 1.25em;
    margin-bottom: 1em;
  }

  p {
    line-height: 1.5em;
  }
`;

interface AssetsIndexProps {
  library: AssetLibrary;
  libraries: AssetLibrary[];
  assets: Asset[];
}

export default function AssetsIndex({ library, assets }: AssetsIndexProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);

  return (
    <Layout title={library ? library.title : "All assets"}>
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

      <AssetList>
        {assets.map((asset) => (
          <AssetCard key={asset.id}>{asset.title}</AssetCard>
        ))}
      </AssetList>
    </Layout>
  );
}
