import { NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import Typography from "@mui/joy/Typography";
import React from "react";
import styled from "styled-components";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
import { Asset, Project } from "../types";

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
      <AssetList>
        {assets.map((asset) => (
          <AssetCard key={asset.id}>{asset.title}</AssetCard>
        ))}
      </AssetList>
    </Layout>
  );
}
