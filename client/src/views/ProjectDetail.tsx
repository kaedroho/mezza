import { NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import {
  Box,
  Dropdown,
  Menu,
  MenuButton,
  MenuItem,
  Typography,
} from "@mui/joy";
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
      <Box px={2} pt={2}>
        <Box
          sx={{
            display: "flex",
            flexFlow: "row wrap",
            flexGrow: 1,
            gap: 2,
          }}
        >
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              gap: 1,
              width: 320,
              height: 240,
              borderRadius: 6,
              alignItems: "center",
              justifyContent: "center",
              border: "2px dashed var(--joy-palette-primary-300)",
            }}
          >
            <Typography
              sx={{
                color: "var(--joy-palette-primary-500)",
                fontWeight: 600,
              }}
            >
              No Thumbnail
            </Typography>
            {/* <Button
              variant="soft"
              color="primary"
              size="sm"
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
              Select thumbnail
            </Button> */}
          </Box>
          <Box
            sx={{
              minWidth: 320,
            }}
          >
            <Typography level="title-md">Release Date</Typography>
            {project.release_date || "Not set"}
            <Typography level="title-md" pt={1}>
              Description
            </Typography>
            {project.description}

            <Box pt={2}>
              <Button
                variant="soft"
                color="primary"
                size="sm"
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
            </Box>
          </Box>
        </Box>

        <Box pt={2}>
          <Typography level="h4">Assets</Typography>
          <Dropdown>
            <MenuButton
              color="primary"
              variant="solid"
              startDecorator={<Add />}
            >
              Add Asset
            </MenuButton>
            <Menu>
              <MenuItem
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
              </MenuItem>
              <MenuItem
                onClick={() =>
                  openOverlay(
                    project.asset_choose_url,
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
                Choose from library
              </MenuItem>
              <MenuItem>Create a Script</MenuItem>
            </Menu>
          </Dropdown>

          <AssetList assets={assets} />
        </Box>
      </Box>
    </Layout>
  );
}
