import { NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import Button from "@mui/joy/Button";
import React from "react";
import FileList from "../components/FileList";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
import { File } from "../types";

interface FileIndexProps {
  upload_url: string;
  files: File[];
}

export default function FileIndex({ upload_url, files }: FileIndexProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);

  return (
    <Layout
      title="Files"
      renderHeaderButtons={() => (
        <Button
          variant="solid"
          color="primary"
          size="sm"
          startDecorator={<Add />}
          onClick={() =>
            openOverlay(
              upload_url,
              (content) => (
                <ModalWindow slideout="right">{content}</ModalWindow>
              ),
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
      <FileList files={files} />
    </Layout>
  );
}
