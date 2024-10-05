import { Form, NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import { Box, Typography } from "@mui/joy";
import Button from "@mui/joy/Button";
import React from "react";
import AssetList from "../components/AssetList";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
import { CSRFTokenContext } from "../contexts";
import { Asset, Project } from "../types";

interface ProjectDetailViewProps {
  project: Project;
  assets: Asset[];
}

export default function ProjectDetailView({
  project,
  assets,
}: ProjectDetailViewProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);
  const csrfToken = React.useContext(CSRFTokenContext);

  return (
    <Layout title={project.title} noIndent>
      <Form action={project.detail_url} method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />

        <Box px={2}>
          <section>
            <Typography level="h4">Basic Information</Typography>
            <Button
              variant="plain"
              color="primary"
              size="sm"
              startDecorator={<Add />}
              onClick={() =>
                openOverlay(
                  project.edit_url,
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
              Edit
            </Button>
            {project.description}
            {project.release_date}
          </section>

          <section>
            <Typography level="h4">Assets</Typography>
            <Button
              variant="plain"
              color="primary"
              size="sm"
              startDecorator={<Add />}
              onClick={() =>
                openOverlay(
                  project.asset_upload_url,
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
            <AssetList assets={assets} />
          </section>

          <Button color="primary" type="submit">
            Save
          </Button>
        </Box>
      </Form>
    </Layout>
  );
}
