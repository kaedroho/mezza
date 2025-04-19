import {
  Link as DjangoBridgeLink,
  NavigationContext,
} from "@django-bridge/react";
import Link from "@mui/joy/Link";
import React from "react";
import styled from "styled-components";
import { File } from "../types";
import ModalWindow from "./ModalWindow";

const Wrapper = styled.ul`
  display: flex;
  flex-flow: row wrap;
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

const ThumbnailImage = styled.img`
  border-radius: 10px;
  height: 240px;
  width: auto;
`;

const ThumbnailVideo = styled.video`
  border-radius: 10px;
`;

const ThumbnailVideoWrapper = styled.div`
  position: relative;
`;

const ThumbnailVideoDuration = styled.div`
  position: absolute;
  bottom: 10px;
  right: 10px;
  color: white;
  font-weight: 500;
  font-size: 0.9em;
  background: rgba(0,0,0,0.7);
  border-radius: 3px;
  padding: 1px 5px;
`;

const ThumbnailPlaceholder = styled.div`
  border-radius: 10px;
  height: 240px;
  width: 180px;
  background-color: var(--variant-plainActiveBg, var(--joy-palette-neutral-plainActiveBg, var(--joy-palette-neutral-200, #DDE7EE)));
`;

interface FileListProps {
  files: File[];
  openInNewTab?: boolean;
  onClickFile?: (file: File) => void;
}

export default function FileList({
  files,
  openInNewTab,
  onClickFile,
}: FileListProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);

  return (
    <Wrapper>
      {files.map((file) => {
        const contents = (
          <CardContent>
            {file.thumbnail_blob && file.thumbnail_blob.content_type.startsWith("image/") && (
              <ThumbnailImage src={file.thumbnail_blob.download_url} width={file.thumbnail_blob.attributes.dimensions?.width} height={file.thumbnail_blob.attributes.dimensions?.height} />
            )}
            {file.thumbnail_blob && file.thumbnail_blob.content_type.startsWith("video/") && (
              <ThumbnailVideoWrapper>
                {/* @ts-ignore */}
                <ThumbnailVideo onMouseOver={(e) => e.target.play()} onMouseLeave={(e) => {e.target.pause(); e.target.currentTime = 0 }} src={file.thumbnail_blob.download_url} width={file.thumbnail_blob.attributes.dimensions?.width} height={file.thumbnail_blob.attributes.dimensions?.height} />
                {file.source_blob.attributes.duration && <ThumbnailVideoDuration>{Math.floor(file.source_blob.attributes.duration / 60)}:{Math.ceil(file.source_blob.attributes.duration % 60).toString().padStart(2, "0")}</ThumbnailVideoDuration>}
              </ThumbnailVideoWrapper>
            )}
            {!file.thumbnail_blob && (
              <ThumbnailPlaceholder />
            )}
            <CardTitle>{file.name}</CardTitle>
            </CardContent>
        );

        return (
          <Card key={file.id}>
            {onClickFile ? (
              <Link component="button" onClick={() => onClickFile(file)}>
                {contents}
              </Link>
            ) : openInNewTab ? (
              <Link component={DjangoBridgeLink} href={file.detail_url}>
                {contents}
              </Link>
            ) : (
              <Link
                component="button"
                onClick={() =>
                  openOverlay(
                    file.detail_url,
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
