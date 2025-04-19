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

const Thumbnail = styled.img`
  border-radius: 10px;
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
            {file.thumbnail_blob && (
              <Thumbnail src={file.thumbnail_blob.download_url} width={file.thumbnail_blob.attributes.dimensions?.width} height={file.thumbnail_blob.attributes.dimensions?.height} />
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
