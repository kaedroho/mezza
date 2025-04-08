import { OverlayContext } from "@django-bridge/react";
import React from "react";
import FileList from "../components/FileList";
import Layout from "../components/Layout";
import { CSRFTokenContext } from "../contexts";
import { File } from "../types";

interface FileChooserViewProps {
  action_url: string;
  files: File[];
}

export default function FileChooserView({
  action_url,
  files,
}: FileChooserViewProps) {
  const { requestClose } = React.useContext(OverlayContext);
  const csrf_token = React.useContext(CSRFTokenContext);

  return (
    <Layout title="Choose File">
      <FileList
        files={files}
        onClickFile={(file) => {
          fetch(action_url, {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
              "X-CSRFToken": csrf_token,
            },
            body: new URLSearchParams({
              file_id: file.id.toString(),
            }),
          }).then(() => requestClose());
        }}
      />
    </Layout>
  );
}
