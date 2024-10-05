import { NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import { Box, Typography } from "@mui/joy";
import Button from "@mui/joy/Button";
import React from "react";
import AssetList from "../components/AssetList";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
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

  return (
    <Layout title={project.title} noIndent>
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
      </Box>
    </Layout>
  );
}
