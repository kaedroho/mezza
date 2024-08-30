import { Form, NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import { Box, Tab, TabList, TabPanel, Tabs } from "@mui/joy";
import Button from "@mui/joy/Button";
import React from "react";
import AssetList from "../components/AssetList";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
import { CSRFTokenContext } from "../contexts";
import FormDef from "../deserializers/Form";
import { Asset, Project } from "../types";

interface ProjectDetailViewProps {
  project: Project;
  basicInfoForm: FormDef;
  scriptForm: FormDef;
  assets: Asset[];
}

export default function ProjectDetailView({
  project,
  basicInfoForm,
  scriptForm,
  assets,
}: ProjectDetailViewProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);
  const csrfToken = React.useContext(CSRFTokenContext);

  return (
    <Layout title={project.title} noIndent>
      <Form action={project.detail_url} method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />

        <Tabs defaultValue={0}>
          <TabList>
            <Tab>Basic Information</Tab>
            <Tab>Script</Tab>
            <Tab>Assets</Tab>
          </TabList>
          <TabPanel value={0} keepMounted>
            {basicInfoForm.render()}
          </TabPanel>
          <TabPanel
            value={1}
            keepMounted
            sx={{ px: 7, label: { display: "none" } }}
          >
            {scriptForm.render()}
          </TabPanel>
          <TabPanel value={2}>
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
          </TabPanel>
        </Tabs>
        <Box px={2}>
          <Button color="primary" type="submit">
            Save
          </Button>
        </Box>
      </Form>
    </Layout>
  );
}
