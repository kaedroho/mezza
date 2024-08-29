import { NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import Typography from "@mui/joy/Typography";
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
    <Layout title={project.title}>
      <Typography level="h2" fontSize="1.2em">
        Basic information
      </Typography>
      <p>{project.description}</p>
      <Typography level="h2" fontSize="1.2em">
        Script
      </Typography>
      <Box
        sx={{
          display: "flex",
          flexFlow: "row nowrap",
          gap: "10px",
          alignItems: "center",
        }}
      >
        <Typography level="h2" fontSize="1.2em">
          Assets
        </Typography>
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
      </Box>
      <AssetList assets={assets} />
    </Layout>
  );
}
