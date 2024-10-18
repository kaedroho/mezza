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
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  list-style: none;
  padding: 0;
`;

const Card = styled.li`
  display: flex;
  justify-content: center;

  h2 {
    font-size: 1.25em;
    margin-bottom: 1em;
  }

  p {
    line-height: 1.5em;
  }
`;

const CardContent = styled.div`
  display: flex;
  flex-direction: column;
`;

const CardTitle = styled.p`
  margin: 0;
  padding: 10px;
`;

const ImageThumbnail = styled.img`
  border-radius: 8px;
  width: 100%;
  object-fit: cover;
`;

const VideoThumbnail = styled.video`
  border-radius: 8px;
  width: 100%;
  object-fit: cover;
`;

interface AssetListProps {
  assets: Asset[];
  openAssetDetailInNewTab?: boolean;
  onClickAsset?: (asset: Asset) => void;
}

export default function AssetList({
  assets,
  openAssetDetailInNewTab,
  onClickAsset,
}: AssetListProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);

  return (
    <Wrapper>
      {assets.map((asset) => {
        const contents = (
          <CardContent>
            {asset.file.thumbnail.type === "image" ? (
              <ImageThumbnail src={asset.file.thumbnail.src} />
            ) : null}
            {asset.file.thumbnail.type === "video" ? (
              <VideoThumbnail controls>
                <source src={asset.file.thumbnail.src} />
              </VideoThumbnail>
            ) : null}
            <CardTitle>{asset.title}</CardTitle>
          </CardContent>
        );

        return (
          <Card key={asset.id}>
            {onClickAsset ? (
              <Link component="button" onClick={() => onClickAsset(asset)}>
                {contents}
              </Link>
            ) : openAssetDetailInNewTab ? (
              <Link component={DjangoBridgeLink} href={asset.detail_url}>
                {contents}
              </Link>
            ) : (
              <Link
                component="button"
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
                {contents}
              </Link>
            )}
          </Card>
        );
      })}
    </Wrapper>
  );
}
