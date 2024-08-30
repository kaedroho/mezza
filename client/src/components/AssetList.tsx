import {
  Link as DjangoBridgeLink,
  NavigationContext,
} from "@django-bridge/react";
import Link from "@mui/joy/Link";
import React from "react";
import styled from "styled-components";
import { Asset } from "../types";
import ModalWindow from "./ModalWindow";

const Wrapper = styled.ul`
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  list-style: none;
  padding: 0;
`;

const Card = styled.li`
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

interface AssetListProps {
  assets: Asset[];
  openAssetDetailInNewTab?: boolean;
}

export default function AssetList({
  assets,
  openAssetDetailInNewTab,
}: AssetListProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);

  return (
    <Wrapper>
      {assets.map((asset) => (
        <Card key={asset.id}>
          {openAssetDetailInNewTab ? (
            <Link component={DjangoBridgeLink} href={asset.detail_url}>
              {asset.title}
            </Link>
          ) : (
            <Link
              component={DjangoBridgeLink}
              href={asset.detail_url}
              onClick={() =>
                openOverlay(
                  asset.detail_url,
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
              {asset.title}
            </Link>
          )}
        </Card>
      ))}
    </Wrapper>
  );
}
